"""
文档加载器模块
支持多种文档格式的加载和解析
"""
from pathlib import Path
from typing import List
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
)
from langchain_core.documents import Document


class DocumentLoader:
    """文档加载器类，支持多种格式"""

    def __init__(self, file_path: str):
        """
        初始化文档加载器

        Args:
            file_path: 文档文件路径或目录路径
        """
        self.file_path = Path(file_path)

    def load(self) -> List[Document]:
        """
        加载文档

        Returns:
            文档列表
        """
        if self.file_path.is_file():
            return self._load_single_file(self.file_path)
        elif self.file_path.is_dir():
            return self._load_directory(self.file_path)
        else:
            raise FileNotFoundError(f"路径不存在: {self.file_path}")

    def _load_single_file(self, file_path: Path) -> List[Document]:
        """加载单个文件"""
        suffix = file_path.suffix.lower()

        try:
            if suffix == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif suffix == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif suffix == '.docx':
                loader = Docx2txtLoader(str(file_path))
            elif suffix in ['.md', '.markdown']:
                loader = UnstructuredMarkdownLoader(str(file_path))
            else:
                raise ValueError(f"不支持的文件格式: {suffix}")

            documents = loader.load()
            print(f"成功加载文件: {file_path.name} ({len(documents)} 个文档)")
            return documents

        except Exception as e:
            print(f"加载文件失败 {file_path.name}: {e}")
            return []

    def _load_directory(self, dir_path: Path) -> List[Document]:
        """加载目录下所有支持的文档"""
        all_documents = []
        supported_extensions = {'.pdf', '.txt', '.docx', '.md', '.markdown'}

        for file_path in dir_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                documents = self._load_single_file(file_path)
                all_documents.extend(documents)

        print(f"目录加载完成，共 {len(all_documents)} 个文档")
        return all_documents


def load_documents(file_path: str) -> List[Document]:
    """
    便捷函数：加载文档

    Args:
        file_path: 文档文件路径或目录路径

    Returns:
        文档列表
    """
    loader = DocumentLoader(file_path)
    return loader.load()
