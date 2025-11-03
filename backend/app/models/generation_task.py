"""生成任务模型"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class GenerationTask(Base):
    """生成任务表"""
    __tablename__ = "generation_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    model_name = Column(String(100), nullable=False)
    status = Column(String(20), default="pending", index=True)  # pending, processing, completed, failed
    result_id = Column(Integer, ForeignKey("results.id"), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<GenerationTask(id={self.id}, user_id={self.user_id}, status={self.status})>"

