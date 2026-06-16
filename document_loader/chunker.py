"""
文本分割模块
将长文档分割成适合向量化的文本块
"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class TextChunker:
    """文本分割器类"""

    def __init__(
            self,
            chunk_size: int = 500,
            chunk_overlap: int = 50,
            separators: List[str] = None
    ):
        """
        初始化文本分割器

        Args:
            chunk_size: 每个文本块的大小（字符数）
            chunk_overlap: 文本块之间的重叠大小
            separators: 分隔符列表，按优先级排序
        """
        if separators is None:
            separators = ["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=len,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        分割文档列表

        Args:
            documents: 文档列表

        Returns:
            分割后的文档块列表
        """
        chunks = self.text_splitter.split_documents(documents)
        print(f"文档分割完成: {len(documents)} 个文档 -> {len(chunks)} 个文本块")
        return chunks

    def split_text(self, text: str) -> List[str]:
        """
        分割纯文本

        Args:
            text: 待分割的文本

        Returns:
            文本块列表
        """
        chunks = self.text_splitter.split_text(text)
        print(f"文本分割完成: {len(chunks)} 个文本块")
        return chunks


def chunk_documents(
        documents: List[Document],
        chunk_size: int = 500,
        chunk_overlap: int = 50
) -> List[Document]:
    """
    便捷函数：分割文档

    Args:
        documents: 文档列表
        chunk_size: 每个文本块的大小
        chunk_overlap: 文本块之间的重叠大小

    Returns:
        分割后的文档块列表
    """
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunker.split_documents(documents)
