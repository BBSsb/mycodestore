# 测试LLM配置
from src.config.llm_config import get_llm_client, LLMConfig

print(f"LLM启用状态: {LLMConfig.is_llm_enabled()}")
print(f"模型: {LLMConfig.get_model()}")

llm = get_llm_client()
if llm:
    response = llm.invoke("你好，请介绍一下自己")
    print(response.content)
