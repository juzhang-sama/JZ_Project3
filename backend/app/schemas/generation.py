"""生成任务相关的Pydantic模型"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GenerationCreateRequest(BaseModel):
    """创建生成任务请求"""
    prompt: str
    model_name: str


class GenerationResponse(BaseModel):
    """生成任务响应"""
    id: int
    user_id: int
    prompt: str
    model_name: str
    status: str
    result_id: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

