"""
ComfyUI服务 - 与ComfyUI API交互
"""
import json
import time
import requests
from typing import Dict, Any, Optional
from app.config import settings


class ComfyUIService:
    """ComfyUI服务类"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8188"):
        """
        初始化ComfyUI服务
        
        Args:
            base_url: ComfyUI API基础URL
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.timeout = 30
    
    def check_connection(self) -> bool:
        """
        检查与ComfyUI的连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            response = requests.get(f"{self.api_url}/system", timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            print(f"ComfyUI连接失败: {e}")
            return False
    
    def get_models(self) -> Dict[str, Any]:
        """
        获取可用的模型列表
        
        Returns:
            Dict: 模型信息
        """
        try:
            response = requests.get(f"{self.api_url}/models", timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"获取模型列表失败: {e}")
            return {}
    
    def submit_prompt(self, prompt: Dict[str, Any]) -> Optional[str]:
        """
        提交生成任务到ComfyUI
        
        Args:
            prompt: 工作流提示词
            
        Returns:
            Optional[str]: 任务ID
        """
        try:
            response = requests.post(
                f"{self.api_url}/prompt",
                json={"prompt": prompt},
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("prompt_id")
            return None
        except Exception as e:
            print(f"提交任务失败: {e}")
            return None
    
    def get_history(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """
        获取任务执行历史
        
        Args:
            prompt_id: 任务ID
            
        Returns:
            Optional[Dict]: 任务历史信息
        """
        try:
            response = requests.get(
                f"{self.api_url}/history/{prompt_id}",
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return data.get(prompt_id)
            return None
        except Exception as e:
            print(f"获取任务历史失败: {e}")
            return None
    
    def wait_for_completion(self, prompt_id: str, max_wait: int = 300) -> Optional[Dict[str, Any]]:
        """
        等待任务完成
        
        Args:
            prompt_id: 任务ID
            max_wait: 最大等待时间（秒）
            
        Returns:
            Optional[Dict]: 任务结果
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            history = self.get_history(prompt_id)
            
            if history:
                # 检查是否有输出
                if "outputs" in history:
                    return history
                
                # 检查是否有错误
                if "status" in history and history["status"].get("status_code") == "error":
                    return None
            
            time.sleep(1)
        
        return None
    
    def get_image_path(self, history: Dict[str, Any], node_id: str = "9") -> Optional[str]:
        """
        从历史记录中获取图像路径
        
        Args:
            history: 任务历史
            node_id: 节点ID（默认为输出节点）
            
        Returns:
            Optional[str]: 图像路径
        """
        try:
            if "outputs" in history and node_id in history["outputs"]:
                outputs = history["outputs"][node_id]
                if "images" in outputs and len(outputs["images"]) > 0:
                    return outputs["images"][0]["filename"]
            return None
        except Exception as e:
            print(f"获取图像路径失败: {e}")
            return None
    
    def generate_image(self, prompt: str, model_name: str = "sd15") -> Optional[Dict[str, Any]]:
        """
        生成图像
        
        Args:
            prompt: 提示词
            model_name: 模型名称
            
        Returns:
            Optional[Dict]: 生成结果
        """
        # 创建工作流
        workflow = self._create_workflow(prompt, model_name)
        
        # 提交任务
        prompt_id = self.submit_prompt(workflow)
        if not prompt_id:
            return None
        
        # 等待完成
        history = self.wait_for_completion(prompt_id)
        if not history:
            return None
        
        # 获取图像路径
        image_path = self.get_image_path(history)
        if not image_path:
            return None
        
        return {
            "prompt_id": prompt_id,
            "image_path": image_path,
            "history": history
        }
    
    def _create_workflow(self, prompt: str, model_name: str) -> Dict[str, Any]:
        """
        创建ComfyUI工作流
        
        Args:
            prompt: 提示词
            model_name: 模型名称
            
        Returns:
            Dict: 工作流配置
        """
        # 基础工作流模板
        workflow = {
            "1": {
                "inputs": {
                    "ckpt_name": f"{model_name}.safetensors"
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "2": {
                "inputs": {
                    "text": prompt,
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                }
            },
            "3": {
                "inputs": {
                    "text": "",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Negative)"
                }
            },
            "4": {
                "inputs": {
                    "width": 512,
                    "height": 512,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage",
                "_meta": {
                    "title": "Empty Latent Image"
                }
            },
            "5": {
                "inputs": {
                    "seed": 0,
                    "steps": 20,
                    "cfg": 7.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["1", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["4", 0]
                },
                "class_type": "KSampler",
                "_meta": {
                    "title": "KSampler"
                }
            },
            "6": {
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2]
                },
                "class_type": "VAEDecode",
                "_meta": {
                    "title": "VAE Decode"
                }
            },
            "7": {
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": ["6", 0]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "Save Image"
                }
            },
            "9": {
                "inputs": {
                    "images": ["6", 0]
                },
                "class_type": "PreviewImage",
                "_meta": {
                    "title": "Preview Image"
                }
            }
        }
        
        return workflow

