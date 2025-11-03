"""
启动Celery Worker
"""
import os
import sys
from app.celery_app import celery_app

if __name__ == "__main__":
    # 启动Celery Worker
    celery_app.worker_main([
        "worker",
        "--loglevel=info",
        "--concurrency=4",
        "--max-tasks-per-child=1000",
    ])

