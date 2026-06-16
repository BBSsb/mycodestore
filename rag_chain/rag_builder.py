"""
RAG 链构建模块
整合检索和生成，实现完整的问答功能
"""
import os
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vector_store.vector_db import VectorDatabase


class RAGChain:
    """RAG 链类"""

    def __init__(
        self,
        persist_directory: str = "chroma_db",
        collection_name: str = "rag_collection",
        model_name: str = "qwen-plus-2025-07-28",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        初始化 RAG 链

        Args:
            persist_directory: 向量数据库持久化目录
            collection_name: 集合名称
            model_name: 大语言模型名称
            api_key: API密钥（可选，默认从环境变量读取）
            base_url: API基础URL（可选，默认从环境变量读取）
            temperature: 温度参数，控制回答的创造性
        """
        # 加载向量数据库
        self.db = VectorDatabase(persist_directory=persist_directory)
        self.db.load_existing(collection_name)

        # 配置 LLM
        if api_key is None:
            api_key = os.getenv("DASHSCOPE_API_KEY")
        if base_url is None:
            base_url = os.getenv("DASHSCOPE_BASE_URL")

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url
        )

        # 定义提示词模板
        self.prompt_template = ChatPromptTemplate.from_template("""
你是一个智能助手，请根据提供的上下文信息来回答用户的问题。

上下文信息：
{context}

用户问题：{question}

请基于以上上下文信息，用中文给出准确、简洁的回答。如果上下文中没有相关信息，请直接说明"根据提供的资料，我无法找到相关答案"。

回答：
""")

        # 构建 RAG 链
        self.retriever = self.db.vector_store.as_retriever(search_kwargs={"k": 5})
        self.rag_chain = self._build_chain()

    def _build_chain(self):
        """构建 RAG 链"""

        def format_docs(docs: List[Document]) -> str:
            """格式化文档"""
            return "\n\n".join([doc.page_content for doc in docs])

        # 构建完整的 RAG 链
        chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )

        return chain

    def ask(self, question: str) -> str:
        """
        提问并获取回答

        Args:
            question: 用户问题

        Returns:
            AI 的回答
        """
        print(f"\n问题: {question}")
        answer = self.rag_chain.invoke(question)
        print(f"回答: {answer}")
        return answer

    def ask_with_sources(self, question: str) -> dict:
        """
        提问并获取回答及来源

        Args:
            question: 用户问题

        Returns:
            包含回答和来源信息的字典
        """
        print(f"\n问题: {question}")

        # 先检索相关文档
        relevant_docs = self.db.search(question, k=5)

        # 生成回答
        answer = self.rag_chain.invoke(question)

        # 构建来源信息
        sources = []
        for i, doc in enumerate(relevant_docs, 1):
            source_info = {
                "index": i,
                "content": doc.page_content[:200],
                "metadata": doc.metadata
            }
            sources.append(source_info)

        result = {
            "question": question,
            "answer": answer,
            "sources": sources
        }

        print(f"回答: {answer}")
        print(f"参考来源: {len(sources)} 个文档")

        return result


def create_rag_chain(
    persist_directory: str = "chroma_db",
    collection_name: str = "rag_collection",
    model_name: str = "qwen-plus-2025-07-28",
    temperature: float = 0.7
) -> RAGChain:
    """
    便捷函数：创建 RAG 链

    Args:
        persist_directory: 向量数据库持久化目录
        collection_name: 集合名称
        model_name: 大语言模型名称
        temperature: 温度参数

    Returns:
        RAG 链实例
    """
    return RAGChain(
        persist_directory=persist_directory,
        collection_name=collection_name,
        model_name=model_name,
        temperature=temperature
    )
