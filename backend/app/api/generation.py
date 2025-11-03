"""
生成API路由
"""
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.generation import GenerationCreateRequest, GenerationResponse
from app.services.generation_service import GenerationService


router = APIRouter(prefix="/api/v1/generation", tags=["generation"])


@router.post("/create", response_model=GenerationResponse)
async def create_generation(
    request: GenerationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建生成任务
    
    Args:
        request: 生成请求
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        GenerationResponse: 生成任务信息
    """
    service = GenerationService(db)
    
    # 创建任务
    task = service.create_task(current_user.id, request.prompt, request.model_name)
    
    if not task:
        raise HTTPException(status_code=400, detail="创建任务失败")
    
    return {
        "id": task.id,
        "user_id": task.user_id,
        "prompt": task.prompt,
        "model_name": task.model_name,
        "status": task.status,
        "result_id": task.result_id,
        "error_message": task.error_message,
        "created_at": task.created_at,
        "completed_at": task.completed_at
    }


@router.get("/status/{task_id}", response_model=GenerationResponse)
async def get_generation_status(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取生成任务状态
    
    Args:
        task_id: 任务ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        GenerationResponse: 生成任务信息
    """
    service = GenerationService(db)
    task = service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 验证权限
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此任务")
    
    return {
        "id": task.id,
        "user_id": task.user_id,
        "prompt": task.prompt,
        "model_name": task.model_name,
        "status": task.status,
        "result_id": task.result_id,
        "error_message": task.error_message,
        "created_at": task.created_at,
        "completed_at": task.completed_at
    }


@router.get("/result/{task_id}")
async def get_generation_result(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取生成结果
    
    Args:
        task_id: 任务ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 生成结果
    """
    service = GenerationService(db)
    task = service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 验证权限
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此任务")
    
    result = service.get_result(task_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="结果不存在")
    
    return {
        "id": result.id,
        "task_id": result.task_id,
        "image_url": result.image_url,
        "image_path": result.image_path,
        "result_metadata": result.result_metadata,
        "created_at": result.created_at
    }


@router.get("/history", response_model=list)
async def get_generation_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取生成历史
    
    Args:
        limit: 限制数量
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        list: 生成历史列表
    """
    service = GenerationService(db)
    tasks = service.get_user_tasks(current_user.id, limit)
    
    return [
        {
            "id": task.id,
            "user_id": task.user_id,
            "prompt": task.prompt,
            "model_name": task.model_name,
            "status": task.status,
            "result_id": task.result_id,
            "error_message": task.error_message,
            "created_at": task.created_at,
            "completed_at": task.completed_at
        }
        for task in tasks
    ]


@router.delete("/{task_id}")
async def delete_generation(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除生成任务
    
    Args:
        task_id: 任务ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 删除结果
    """
    service = GenerationService(db)
    task = service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 验证权限
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此任务")
    
    if service.delete_task(task_id):
        return {"message": "任务已删除"}
    else:
        raise HTTPException(status_code=400, detail="删除失败")


def generate_image_background(task_id: int, db_session):
    """后台生成图像"""
    from app.models.generation_task import GenerationTask
    from app.services.comfyui_service import ComfyUIService

    try:
        db = db_session
        task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
        if not task:
            return

        # 更新状态为处理中
        task.status = "processing"
        db.commit()

        # 创建ComfyUI服务
        comfyui_service = ComfyUIService()

        # 检查连接
        if not comfyui_service.check_connection():
            task.status = "failed"
            task.error_message = "ComfyUI连接失败"
            db.commit()
            return

        # 生成图像
        result = comfyui_service.generate_image(task.prompt, task.model_name)
        if not result:
            task.status = "failed"
            task.error_message = "图像生成失败"
            db.commit()
            return

        # 保存结果
        service = GenerationService(db)
        result_obj = service.save_result(
            task_id=task_id,
            image_path=result.get("image_path"),
            image_url=f"/api/v1/results/{task_id}/image",
            result_metadata=result,
        )

        # 更新任务状态为完成
        task.status = "completed"
        task.result_id = result_obj.id if result_obj else None
        db.commit()

    except Exception as e:
        task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
        if task:
            task.status = "failed"
            task.error_message = str(e)
            db.commit()


@router.post("/create-async", response_model=GenerationResponse)
async def create_generation_async(
    request: GenerationCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建异步生成任务

    Args:
        request: 生成请求
        background_tasks: 后台任务
        current_user: 当前用户
        db: 数据库会话

    Returns:
        GenerationResponse: 生成任务信息
    """
    service = GenerationService(db)

    # 创建任务
    task = service.create_task(current_user.id, request.prompt, request.model_name)

    if not task:
        raise HTTPException(status_code=400, detail="创建任务失败")

    # 添加后台任务
    background_tasks.add_task(generate_image_background, task.id, db)

    return {
        "id": task.id,
        "user_id": task.user_id,
        "prompt": task.prompt,
        "model_name": task.model_name,
        "status": task.status,
        "result_id": task.result_id,
        "error_message": task.error_message,
        "created_at": task.created_at,
        "completed_at": task.completed_at
    }

