"""
向量数据库模块
使用 ChromaDB 存储和检索文档向量
"""
import os
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


class VectorDatabase:
    """向量数据库类"""

    def __init__(
        self,
        persist_directory: str = "chroma_db",
        embedding_model: str = "text-embedding-v3",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        初始化向量数据库

        Args:
            persist_directory: 向量数据库持久化目录
            embedding_model: 嵌入模型名称
            api_key: API密钥（可选，默认从环境变量读取）
            base_url: API基础URL（可选，默认从环境变量读取）
        """
        self.persist_directory = persist_directory

        # 配置嵌入模型
        if api_key is None:
            api_key = os.getenv("DASHSCOPE_API_KEY")
        if base_url is None:
            base_url = os.getenv("DASHSCOPE_BASE_URL")

        # 检查 API 密钥是否存在
        if not api_key:
            raise ValueError(
                "未找到 API 密钥！请设置 DASHSCOPE_API_KEY 环境变量或在初始化时传入 api_key 参数"
            )

        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            api_key=api_key,
            base_url=base_url,
            check_embedding_ctx_length=False,
            tiktoken_model_name=embedding_model
        )

        # 初始化向量数据库
        self.vector_store = None

    def from_documents(
        self,
        documents: List[Document],
        collection_name: str = "rag_collection"
    ):
        """
        从文档列表创建向量数据库

        Args:
            documents: 文档列表
            collection_name: 集合名称
        """
        print(f"正在创建向量数据库...")
        print(f"  - 文档数量: {len(documents)}")
        print(f"  - 集合名称: {collection_name}")
        print(f"  - 持久化目录: {self.persist_directory}")

        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=self.persist_directory
        )

        print(f"向量数据库创建成功！")
        return self.vector_store

    def load_existing(
        self,
        collection_name: str = "rag_collection"
    ):
        """
        加载已存在的向量数据库

        Args:
            collection_name: 集合名称

        Returns:
            向量数据库实例
        """
        print(f"正在加载向量数据库...")
        print(f"  - 集合名称: {collection_name}")
        print(f"  - 持久化目录: {self.persist_directory}")

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        print(f"向量数据库加载成功！")
        return self.vector_store

    def search(
        self,
        query: str,
        k: int = 5
    ) -> List[Document]:
        """
        搜索相似文档

        Args:
            query: 查询文本
            k: 返回的最相似文档数量

        Returns:
            相似文档列表
        """
        if self.vector_store is None:
            raise ValueError("向量数据库未初始化，请先创建或加载数据库")

        print(f"正在搜索: {query[:50]}...")
        results = self.vector_store.similarity_search(query, k=k)
        print(f"找到 {len(results)} 个相似文档")

        return results

    def search_with_score(
        self,
        query: str,
        k: int = 5
    ) -> List[tuple]:
        """
        搜索相似文档并返回相似度分数

        Args:
            query: 查询文本
            k: 返回的最相似文档数量

        Returns:
            (文档, 分数) 元组列表，分数越低越相似
        """
        if self.vector_store is None:
            raise ValueError("向量数据库未初始化，请先创建或加载数据库")

        print(f"正在搜索（带分数）: {query[:50]}...")
        results = self.vector_store.similarity_search_with_score(query, k=k)
        print(f"找到 {len(results)} 个相似文档")

        return results

    def add_documents(
        self,
        documents: List[Document]
    ):
        """
        向数据库添加新文档

        Args:
            documents: 要添加的文档列表
        """
        if self.vector_store is None:
            raise ValueError("向量数据库未初始化，请先创建或加载数据库")

        print(f"正在添加 {len(documents)} 个文档...")
        self.vector_store.add_documents(documents)
        print(f"文档添加成功！")

    def delete_collection(self, collection_name: str = "rag_collection"):
        """
        删除集合

        Args:
            collection_name: 要删除的集合名称
        """
        if self.vector_store is None:
            self.load_existing(collection_name)

        print(f"正在删除集合: {collection_name}")
        self.vector_store.delete_collection()
        print(f"集合删除成功！")


def create_vector_db(
    documents: List[Document],
    persist_directory: str = "chroma_db",
    collection_name: str = "rag_collection"
) -> Chroma:
    """
    便捷函数：创建向量数据库

    Args:
        documents: 文档列表
        persist_directory: 持久化目录
        collection_name: 集合名称

    Returns:
        向量数据库实例
    """
    db = VectorDatabase(persist_directory=persist_directory)
    return db.from_documents(documents, collection_name)


def search_documents(
    query: str,
    persist_directory: str = "chroma_db",
    collection_name: str = "rag_collection",
    k: int = 5
) -> List[Document]:
    """
    便捷函数：搜索文档

    Args:
        query: 查询文本
        persist_directory: 持久化目录
        collection_name: 集合名称
        k: 返回的文档数量

    Returns:
        相似文档列表
    """
    db = VectorDatabase(persist_directory=persist_directory)
    db.load_existing(collection_name)
    return db.search(query, k=k)
