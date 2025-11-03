"""数据库初始化脚本"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 添加app目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from app.database import Base
from app.models.user import User
from app.models.model import Model
from app.models.generation_task import GenerationTask
from app.models.result import Result
from app.config import settings


def init_db():
    """初始化数据库"""
    print("🔧 开始初始化数据库...")
    
    # 创建引擎
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    # 创建所有表
    print("📝 创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")
    
    # 创建会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 检查是否已有默认模型
        existing_models = db.query(Model).count()
        
        if existing_models == 0:
            print("📝 插入默认模型...")
            
            # 创建默认模型
            models = [
                Model(
                    name="stable-diffusion-1.5",
                    display_name="Stable Diffusion 1.5",
                    description="基础的Stable Diffusion 1.5模型",
                    model_path="models/checkpoints/sd-v1-5.safetensors",
                    is_active=True,
                    is_default=True
                ),
                Model(
                    name="stable-diffusion-xl",
                    display_name="Stable Diffusion XL",
                    description="高质量的SDXL模型",
                    model_path="models/checkpoints/sd-xl-base-1.0.safetensors",
                    is_active=True,
                    is_default=False
                ),
                Model(
                    name="dreamshaper",
                    display_name="DreamShaper",
                    description="艺术风格的DreamShaper模型",
                    model_path="models/checkpoints/dreamshaper_8.safetensors",
                    is_active=True,
                    is_default=False
                ),
            ]
            
            for model in models:
                db.add(model)
            
            db.commit()
            print("✅ 默认模型插入完成")
        else:
            print(f"ℹ️  数据库中已有 {existing_models} 个模型，跳过插入")
        
        print("\n✅ 数据库初始化完成！")
        print("\n📊 数据库统计：")
        print(f"  - 用户数：{db.query(User).count()}")
        print(f"  - 模型数：{db.query(Model).count()}")
        print(f"  - 生成任务数：{db.query(GenerationTask).count()}")
        print(f"  - 结果数：{db.query(Result).count()}")
        
    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

