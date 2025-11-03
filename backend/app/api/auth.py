"""认证API路由"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    UserProfileUpdateRequest,
    RefreshTokenRequest,
)
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token, verify_token, get_user_id_from_token
from app.exceptions.auth import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidTokenException,
    WeakPasswordException,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """获取当前用户"""
    token = getattr(request.state, "token", None)

    if not token:
        raise InvalidTokenException()

    user_id = get_user_id_from_token(token)
    if not user_id:
        raise InvalidTokenException()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()

    return user


@router.post("/register", response_model=UserResponse)
async def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    """用户注册"""
    # 检查邮箱是否已存在
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise UserAlreadyExistsException(request.email)
    
    # 检查用户名是否已存在
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {request.username} already exists",
        )
    
    # 检查密码强度
    if len(request.password) < 8:
        raise WeakPasswordException()
    
    # 创建新用户
    user = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        is_active=True,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """用户登录"""
    # 查找用户
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise InvalidCredentialsException()
    
    # 验证密码
    if not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsException()
    
    # 检查用户是否激活
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # 生成令牌
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    request: Request,
    db: Session = Depends(get_db),
):
    """获取当前用户信息"""
    user = get_current_user(request, db)
    return user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_request: UserProfileUpdateRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """更新用户信息"""
    user = get_current_user(request, db)

    if profile_request.username:
        # 检查用户名是否已被使用
        existing = db.query(User).filter(
            User.username == profile_request.username,
            User.id != user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        user.username = profile_request.username

    if profile_request.avatar_url:
        user.avatar_url = profile_request.avatar_url
    
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """刷新令牌"""
    payload = verify_token(request.refresh_token)
    if not payload:
        raise InvalidTokenException()
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    
    # 生成新的访问令牌
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db),
):
    """用户登出"""
    user = get_current_user(request, db)
    return {"message": "Logged out successfully"}

