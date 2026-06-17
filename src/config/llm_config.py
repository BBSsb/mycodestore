"""
LLM配置模块
支持通义千问等国内大模型
"""

import os
import json
from dotenv import load_dotenv
from typing import Optional

# 加载环境变量
load_dotenv()


class LLMConfig:
    """LLM配置类"""

    # 是否使用LLM
    USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"

    # API配置
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

    # 模型选择
    LLM_MODEL = os.getenv("LLM_MODEL", "qwen-turbo")

    # 温度参数
    TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

    @classmethod
    def is_llm_enabled(cls) -> bool:
        """检查是否启用了LLM"""
        return cls.USE_LLM and bool(cls.DASHSCOPE_API_KEY)

    @classmethod
    def get_api_key(cls) -> str:
        """获取API Key"""
        return cls.DASHSCOPE_API_KEY

    @classmethod
    def get_model(cls) -> str:
        """获取模型名称"""
        return cls.LLM_MODEL


class DashScopeLLMWrapper:
    """
    DashScope LLM包装器
    直接使用dashscope SDK
    """

    def __init__(self, model: str, api_key: str, temperature: float = 0.7):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature

        # 设置API Key
        import dashscope
        dashscope.api_key = api_key

    def invoke(self, prompt: str) -> 'LLMResponse':
        """
        调用LLM

        Args:
            prompt: 提示文本

        Returns:
            LLM响应对象
        """
        from dashscope import Generation

        response = Generation.call(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=self.temperature
        )

        if response.status_code == 200:
            return LLMResponse(content=response.output.text)
        else:
            raise Exception(f"LLM调用失败: {response.message}")


class LLMResponse:
    """简单的LLM响应对象"""
    def __init__(self, content: str):
        self.content = content


def get_llm_client():
    """
    获取LLM客户端实例

    Returns:
        LLM客户端实例或None
    """
    if not LLMConfig.is_llm_enabled():
        print("⚠️  LLM未启用或API Key未配置，将使用规则模式")
        return None

    try:
        # 使用原生DashScope SDK
        llm = DashScopeLLMWrapper(
            model=LLMConfig.get_model(),
            api_key=LLMConfig.get_api_key(),
            temperature=LLMConfig.TEMPERATURE
        )

        print(f"✅ 成功加载通义千问模型: {LLMConfig.get_model()}")
        return llm

    except Exception as e:
        print(f"❌ 初始化LLM失败: {e}")
        print("请确保已安装dashscope: pip install dashscope")
        return None
