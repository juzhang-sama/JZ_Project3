"""
生成服务 - 处理图像生成业务逻辑
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.generation_task import GenerationTask
from app.models.result import Result
from app.models.user import User
from app.models.model import Model
from app.services.comfyui_service import ComfyUIService
from datetime import datetime


class GenerationService:
    """生成服务类"""
    
    def __init__(self, db: Session):
        """
        初始化生成服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.comfyui = ComfyUIService()
    
    def create_task(self, user_id: int, prompt: str, model_name: str) -> Optional[GenerationTask]:
        """
        创建生成任务
        
        Args:
            user_id: 用户ID
            prompt: 提示词
            model_name: 模型名称
            
        Returns:
            Optional[GenerationTask]: 创建的任务
        """
        try:
            # 验证用户存在
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            # 验证模型存在
            model = self.db.query(Model).filter(Model.name == model_name).first()
            if not model:
                return None
            
            # 创建任务
            task = GenerationTask(
                user_id=user_id,
                prompt=prompt,
                model_name=model_name,
                status="pending"
            )
            
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            
            return task
        except Exception as e:
            self.db.rollback()
            print(f"创建任务失败: {e}")
            return None
    
    def get_task(self, task_id: int) -> Optional[GenerationTask]:
        """
        获取任务信息
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[GenerationTask]: 任务信息
        """
        return self.db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
    
    def get_user_tasks(self, user_id: int, limit: int = 10) -> list:
        """
        获取用户的任务列表
        
        Args:
            user_id: 用户ID
            limit: 限制数量
            
        Returns:
            list: 任务列表
        """
        return self.db.query(GenerationTask).filter(
            GenerationTask.user_id == user_id
        ).order_by(GenerationTask.created_at.desc()).limit(limit).all()
    
    def update_task_status(self, task_id: int, status: str, error_message: str = None) -> bool:
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            error_message: 错误信息
            
        Returns:
            bool: 是否成功
        """
        try:
            task = self.get_task(task_id)
            if not task:
                return False
            
            task.status = status
            if error_message:
                task.error_message = error_message
            
            if status == "completed":
                task.completed_at = datetime.utcnow()
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"更新任务状态失败: {e}")
            return False
    
    def save_result(self, task_id: int, image_url: str, image_path: str, metadata: Dict[str, Any] = None) -> Optional[Result]:
        """
        保存生成结果
        
        Args:
            task_id: 任务ID
            image_url: 图像URL
            image_path: 图像路径
            metadata: 元数据
            
        Returns:
            Optional[Result]: 保存的结果
        """
        try:
            result = Result(
                task_id=task_id,
                image_url=image_url,
                image_path=image_path,
                result_metadata=metadata or {}
            )
            
            self.db.add(result)
            
            # 更新任务的result_id
            task = self.get_task(task_id)
            if task:
                task.result_id = result.id
            
            self.db.commit()
            self.db.refresh(result)
            
            return result
        except Exception as e:
            self.db.rollback()
            print(f"保存结果失败: {e}")
            return None
    
    def get_result(self, task_id: int) -> Optional[Result]:
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[Result]: 任务结果
        """
        return self.db.query(Result).filter(Result.task_id == task_id).first()
    
    def delete_task(self, task_id: int) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功
        """
        try:
            task = self.get_task(task_id)
            if not task:
                return False
            
            # 删除关联的结果
            result = self.get_result(task_id)
            if result:
                self.db.delete(result)
            
            # 删除任务
            self.db.delete(task)
            self.db.commit()
            
            return True
        except Exception as e:
            self.db.rollback()
            print(f"删除任务失败: {e}")
            return False
    
    def generate_image(self, task_id: int) -> bool:
        """
        生成图像（同步方式）
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功
        """
        try:
            task = self.get_task(task_id)
            if not task:
                return False
            
            # 更新状态为处理中
            self.update_task_status(task_id, "processing")
            
            # 调用ComfyUI生成图像
            result = self.comfyui.generate_image(task.prompt, task.model_name)
            
            if not result:
                self.update_task_status(task_id, "failed", "生成失败")
                return False
            
            # 保存结果
            image_url = f"/api/v1/generation/images/{result['image_path']}"
            self.save_result(
                task_id,
                image_url,
                result['image_path'],
                {"prompt_id": result['prompt_id']}
            )
            
            # 更新状态为完成
            self.update_task_status(task_id, "completed")
            
            return True
        except Exception as e:
            self.update_task_status(task_id, "failed", str(e))
            print(f"生成图像失败: {e}")
            return False

