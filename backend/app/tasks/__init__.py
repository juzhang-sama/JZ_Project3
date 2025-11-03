"""异步任务定义"""
import logging
from typing import Optional, Dict, Any
from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.generation_task import GenerationTask
from app.models.result import Result
from app.services.comfyui_service import ComfyUIService
from app.services.generation_service import GenerationService

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.generate_image")
def generate_image_task(
    self,
    task_id: int,
    prompt: str,
    model_name: str,
    user_id: int,
) -> Dict[str, Any]:
    """
    异步生成图像任务

    Args:
        task_id: 生成任务ID
        prompt: 提示词
        model_name: 模型名称
        user_id: 用户ID

    Returns:
        生成结果
    """
    db = SessionLocal()
    try:
        # 更新任务状态为处理中
        task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
        if not task:
            logger.error(f"Task {task_id} not found")
            return {"status": "failed", "error": "Task not found"}

        task.status = "processing"
        db.commit()

        # 更新任务进度
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 1,
                "total": 3,
                "status": "正在连接ComfyUI...",
                "task_id": task_id,
            }
        )

        # 创建ComfyUI服务
        comfyui_service = ComfyUIService()

        # 检查连接
        if not comfyui_service.check_connection():
            logger.error("ComfyUI connection failed")
            task.status = "failed"
            task.error_message = "ComfyUI连接失败"
            db.commit()
            return {"status": "failed", "error": "ComfyUI connection failed"}

        # 更新进度
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 2,
                "total": 3,
                "status": "正在生成图像...",
                "task_id": task_id,
            }
        )

        # 生成图像
        result = comfyui_service.generate_image(prompt, model_name)
        if not result:
            logger.error(f"Image generation failed for task {task_id}")
            task.status = "failed"
            task.error_message = "图像生成失败"
            db.commit()
            return {"status": "failed", "error": "Image generation failed"}

        # 更新进度
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 3,
                "total": 3,
                "status": "正在保存结果...",
                "task_id": task_id,
            }
        )

        # 保存结果
        generation_service = GenerationService(db)
        result_obj = generation_service.save_result(
            task_id=task_id,
            image_path=result.get("image_path"),
            image_url=f"/api/v1/results/{task_id}/image",
            result_metadata=result,
        )

        # 更新任务状态为完成
        task.status = "completed"
        task.result_id = result_obj.id if result_obj else None
        db.commit()

        logger.info(f"Task {task_id} completed successfully")

        return {
            "status": "completed",
            "task_id": task_id,
            "result_id": result_obj.id if result_obj else None,
            "image_path": result.get("image_path"),
        }

    except Exception as e:
        logger.error(f"Error in generate_image_task: {str(e)}")
        task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
        if task:
            task.status = "failed"
            task.error_message = str(e)
            db.commit()

        return {
            "status": "failed",
            "error": str(e),
            "task_id": task_id,
        }

    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.check_task_status")
def check_task_status(self, task_id: int) -> Dict[str, Any]:
    """
    检查任务状态

    Args:
        task_id: 生成任务ID

    Returns:
        任务状态
    """
    db = SessionLocal()
    try:
        task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
        if not task:
            return {"status": "not_found", "task_id": task_id}

        return {
            "task_id": task_id,
            "status": task.status,
            "prompt": task.prompt,
            "model_name": task.model_name,
            "result_id": task.result_id,
            "error_message": task.error_message,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        }

    except Exception as e:
        logger.error(f"Error in check_task_status: {str(e)}")
        return {"status": "error", "error": str(e), "task_id": task_id}

    finally:
        db.close()


@celery_app.task(name="app.tasks.cleanup_old_tasks")
def cleanup_old_tasks() -> Dict[str, Any]:
    """
    清理旧任务（定期任务）

    Returns:
        清理结果
    """
    from datetime import datetime, timedelta

    db = SessionLocal()
    try:
        # 删除7天前的已完成任务
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        deleted_count = db.query(GenerationTask).filter(
            GenerationTask.status == "completed",
            GenerationTask.completed_at < cutoff_date,
        ).delete()

        db.commit()
        logger.info(f"Cleaned up {deleted_count} old tasks")

        return {"status": "success", "deleted_count": deleted_count}

    except Exception as e:
        logger.error(f"Error in cleanup_old_tasks: {str(e)}")
        return {"status": "error", "error": str(e)}

    finally:
        db.close()

