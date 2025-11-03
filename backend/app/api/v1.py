"""API v1 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.model import Model
from app.models.generation_task import GenerationTask
from app.models.result import Result
from app.schemas.generation import GenerationCreateRequest, GenerationResponse

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": "0.1.0"}


@router.get("/models")
async def get_models(db: Session = Depends(get_db)):
    """获取所有可用模型"""
    models = db.query(Model).filter(Model.is_active == True).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "display_name": m.display_name,
            "description": m.description,
            "is_default": m.is_default,
        }
        for m in models
    ]


@router.post("/generation/create")
async def create_generation_task(
    request: GenerationCreateRequest,
    db: Session = Depends(get_db),
):
    """创建生成任务"""
    # 验证模型是否存在
    model = db.query(Model).filter(Model.name == request.model_name).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # 创建任务
    task = GenerationTask(
        user_id=1,  # 暂时使用固定用户ID
        prompt=request.prompt,
        model_name=request.model_name,
        status="pending",
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return GenerationResponse.from_orm(task).dict()


@router.get("/generation/status/{task_id}")
async def get_task_status(task_id: int, db: Session = Depends(get_db)):
    """获取任务状态"""
    task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return GenerationResponse.from_orm(task).dict()


@router.get("/generation/result/{task_id}")
async def get_task_result(task_id: int, db: Session = Depends(get_db)):
    """获取任务结果"""
    task = db.query(GenerationTask).filter(GenerationTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.result_id is None:
        raise HTTPException(status_code=404, detail="Result not found")

    result = db.query(Result).filter(Result.id == task.result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "id": result.id,
        "task_id": result.task_id,
        "image_url": result.image_url,
        "image_path": result.image_path,
        "created_at": result.created_at.isoformat(),
    }


@router.get("/generation/history")
async def get_history(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
):
    """获取生成历史"""
    skip = (page - 1) * page_size
    tasks = (
        db.query(GenerationTask)
        .order_by(GenerationTask.created_at.desc())
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return [GenerationResponse.from_orm(task).dict() for task in tasks]

