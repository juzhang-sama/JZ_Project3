"""密码加密和验证工具"""

import hashlib
import secrets
from typing import Tuple


def hash_password(password: str) -> str:
    """
    使用PBKDF2加密密码
    
    Args:
        password: 原始密码
        
    Returns:
        加密后的密码（格式：salt$hash）
    """
    # 生成随机盐
    salt = secrets.token_hex(32)
    
    # 使用PBKDF2加密
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # 迭代次数
    )
    
    # 返回盐和哈希值的组合
    return f"{salt}${pwd_hash.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        password: 原始密码
        hashed_password: 加密后的密码
        
    Returns:
        密码是否正确
    """
    try:
        # 分离盐和哈希值
        salt, pwd_hash = hashed_password.split('$')
        
        # 使用相同的盐重新加密
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        # 比较哈希值
        return new_hash.hex() == pwd_hash
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def generate_password() -> str:
    """
    生成随机密码
    
    Returns:
        随机密码
    """
    return secrets.token_urlsafe(16)

