"""生成结果模型"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base


class Result(Base):
    """生成结果表"""
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("generation_tasks.id"), nullable=False, index=True)
    image_url = Column(String(255), nullable=False)
    image_path = Column(String(255), nullable=True)
    result_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Result(id={self.id}, task_id={self.task_id})>"

