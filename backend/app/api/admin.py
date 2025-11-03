"""管理员API路由"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserLoginRequest, TokenResponse, UserResponse
from app.utils.password import verify_password
from app.utils.jwt import create_access_token, create_refresh_token, get_user_id_from_token
from app.exceptions.auth import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserNotFoundException,
    AdminAccessDeniedException,
    InsufficientPermissionsException,
)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


def get_current_admin(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """获取当前管理员用户"""
    token = getattr(request.state, "token", None)

    if not token:
        raise InvalidTokenException()

    user_id = get_user_id_from_token(token)
    if not user_id:
        raise InvalidTokenException()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()

    # 检查是否是管理员
    if not user.is_admin or user.role not in ["admin", "superadmin"]:
        raise AdminAccessDeniedException()

    return user


@router.post("/login", response_model=TokenResponse)
async def admin_login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """管理员登录"""
    # 查找用户
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise InvalidCredentialsException()

    # 验证密码
    if not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsException()

    # 检查是否是管理员
    if not user.is_admin or user.role not in ["admin", "superadmin"]:
        raise AdminAccessDeniedException()

    # 创建令牌
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
async def get_admin_profile(
    current_user: User = Depends(get_current_admin),
):
    """获取管理员个人信息"""
    return current_user


@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取仪表板统计信息"""
    from app.models.generation_task import GenerationTask
    from app.models.model import Model

    # 获取统计信息
    total_users = db.query(User).count()
    total_tasks = db.query(GenerationTask).count()
    total_models = db.query(Model).count()
    
    # 获取任务状态统计
    completed_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "completed"
    ).count()
    failed_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "failed"
    ).count()
    pending_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "pending"
    ).count()
    processing_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "processing"
    ).count()

    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "total_models": total_models,
        "task_stats": {
            "completed": completed_tasks,
            "failed": failed_tasks,
            "pending": pending_tasks,
            "processing": processing_tasks,
        },
    }


@router.get("/users")
async def list_users(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取用户列表"""
    users = db.query(User).offset(skip).limit(limit).all()
    total = db.query(User).count()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": users,
    }


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_detail(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取用户详情"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    
    return user


@router.patch("/users/{user_id}")
async def update_user(
    user_id: int,
    data: dict,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()

    # 只有超级管理员可以修改其他管理员
    if user.is_admin and current_user.role != "superadmin":
        raise InsufficientPermissionsException()

    # 更新允许的字段
    allowed_fields = ["is_active", "role"]
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])

    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """删除用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()

    # 不能删除管理员
    if user.is_admin:
        raise InsufficientPermissionsException()

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


@router.get("/tasks")
async def list_tasks(
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取任务列表"""
    from app.models.generation_task import GenerationTask

    query = db.query(GenerationTask)

    if status:
        query = query.filter(GenerationTask.status == status)

    tasks = query.offset(skip).limit(limit).all()
    total = query.count()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "tasks": tasks,
    }


@router.get("/tasks/{task_id}")
async def get_task_detail(
    task_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取任务详情"""
    from app.models.generation_task import GenerationTask

    task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/models")
async def list_models(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取模型列表"""
    from app.models.model import Model

    models = db.query(Model).offset(skip).limit(limit).all()
    total = db.query(Model).count()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "models": models,
    }


@router.patch("/models/{model_id}")
async def update_model(
    model_id: int,
    data: dict,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """更新模型信息"""
    from app.models.model import Model

    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # 更新允许的字段
    allowed_fields = ["is_active", "is_default", "display_name", "description"]
    for field in allowed_fields:
        if field in data:
            setattr(model, field, data[field])

    db.commit()
    db.refresh(model)

    return model


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """删除任务"""
    from app.models.generation_task import GenerationTask

    task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}


@router.get("/tasks/status/{status}")
async def get_tasks_by_status(
    status: str,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """按状态获取任务"""
    from app.models.generation_task import GenerationTask

    query = db.query(GenerationTask).filter(GenerationTask.status == status)
    tasks = query.offset(skip).limit(limit).all()
    total = query.count()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "status": status,
        "tasks": tasks,
    }


@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取系统统计信息"""
    from app.models.generation_task import GenerationTask
    from app.models.model import Model
    from datetime import datetime, timedelta

    # 总体统计
    total_users = db.query(User).count()
    total_tasks = db.query(GenerationTask).count()
    total_models = db.query(Model).count()

    # 任务状态统计
    completed_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "completed"
    ).count()
    failed_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "failed"
    ).count()
    pending_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "pending"
    ).count()
    processing_tasks = db.query(GenerationTask).filter(
        GenerationTask.status == "processing"
    ).count()

    # 今日统计
    today = datetime.utcnow().date()
    today_tasks = db.query(GenerationTask).filter(
        GenerationTask.created_at >= datetime.combine(today, datetime.min.time())
    ).count()

    # 活跃用户（有任务的用户）
    active_users = db.query(GenerationTask.user_id).distinct().count()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_tasks": total_tasks,
        "total_models": total_models,
        "today_tasks": today_tasks,
        "task_stats": {
            "completed": completed_tasks,
            "failed": failed_tasks,
            "pending": pending_tasks,
            "processing": processing_tasks,
        },
        "success_rate": round(
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2
        ),
    }


@router.post("/models")
async def create_model(
    data: dict,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """创建新模型"""
    from app.models.model import Model

    # 检查模型是否已存在
    existing = db.query(Model).filter(Model.name == data.get("name")).first()
    if existing:
        raise HTTPException(status_code=400, detail="Model already exists")

    model = Model(
        name=data.get("name"),
        display_name=data.get("display_name", data.get("name")),
        description=data.get("description", ""),
        model_path=data.get("model_path", ""),
        is_active=data.get("is_active", True),
        is_default=data.get("is_default", False),
    )

    db.add(model)
    db.commit()
    db.refresh(model)

    return model


@router.get("/models/{model_id}")
async def get_model_detail(
    model_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取模型详情"""
    from app.models.model import Model

    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    return model


@router.delete("/models/{model_id}")
async def delete_model(
    model_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """删除模型"""
    from app.models.model import Model

    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    db.delete(model)
    db.commit()

    return {"message": "Model deleted successfully"}


@router.get("/models/{model_id}/toggle")
async def toggle_model_status(
    model_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """切换模型启用/禁用状态"""
    from app.models.model import Model

    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    model.is_active = not model.is_active
    db.commit()
    db.refresh(model)

    return model

