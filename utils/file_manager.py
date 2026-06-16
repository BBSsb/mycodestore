"""
文件管理模块
处理文件上传、保存和管理
"""
import os
import shutil
from pathlib import Path
from typing import List


class FileManager:
    """文件管理器类"""

    def __init__(self, upload_dir: str = "docs"):
        """
        初始化文件管理器

        Args:
            upload_dir: 上传文件保存目录
        """
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

        # 支持的文件格式
        self.supported_formats = {
            '.pdf', '.txt', '.docx', '.md', '.markdown'
        }

    def save_uploaded_file(self, uploaded_file, file_path: str = None) -> str:
        """
        保存上传的文件

        Args:
            uploaded_file: Streamlit UploadedFile 对象或文件路径
            file_path: 自定义保存路径（可选）

        Returns:
            保存后的文件路径
        """
        if hasattr(uploaded_file, 'name'):
            # Streamlit UploadedFile 对象
            filename = uploaded_file.name
            file_bytes = uploaded_file.getvalue()
        else:
            # 文件路径字符串
            filename = os.path.basename(str(uploaded_file))
            with open(uploaded_file, 'rb') as f:
                file_bytes = f.read()

        # 检查文件格式
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {file_ext}")

        # 生成保存路径
        if file_path is None:
            save_path = self.upload_dir / filename
        else:
            save_path = Path(file_path)

        # 如果文件已存在，添加数字后缀
        if save_path.exists():
            base_name = save_path.stem
            counter = 1
            while save_path.exists():
                new_name = f"{base_name}_{counter}{file_ext}"
                save_path = self.upload_dir / new_name
                counter += 1

        # 保存文件
        with open(save_path, 'wb') as f:
            f.write(file_bytes)

        return str(save_path)

    def save_multiple_files(self, uploaded_files) -> List[str]:
        """
        保存多个上传的文件

        Args:
            uploaded_files: Streamlit UploadedFile 列表

        Returns:
            保存后的文件路径列表
        """
        saved_paths = []

        for uploaded_file in uploaded_files:
            try:
                save_path = self.save_uploaded_file(uploaded_file)
                saved_paths.append(save_path)
            except Exception as e:
                print(f"保存文件 {uploaded_file.name} 失败: {e}")

        return saved_paths

    def list_files(self) -> List[Path]:
        """
        列出所有已上传的文件

        Returns:
            文件路径列表
        """
        if not self.upload_dir.exists():
            return []

        files = []
        for file_path in self.upload_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                files.append(file_path)

        return sorted(files)

    def delete_file(self, filename: str) -> bool:
        """
        删除指定文件

        Args:
            filename: 文件名

        Returns:
            是否删除成功
        """
        file_path = self.upload_dir / filename

        if file_path.exists():
            file_path.unlink()
            return True

        return False

    def clear_all_files(self) -> int:
        """
        清空所有文件

        Returns:
            删除的文件数量
        """
        if not self.upload_dir.exists():
            return 0

        count = 0
        for file_path in self.upload_dir.iterdir():
            if file_path.is_file():
                file_path.unlink()
                count += 1

        return count

    def get_file_count(self) -> int:
        """
        获取文件数量

        Returns:
            文件数量
        """
        return len(self.list_files())

    def get_supported_formats_str(self) -> str:
        """
        获取支持的文件格式字符串

        Returns:
            格式字符串，如 "PDF, TXT, DOCX, MD"
        """
        formats = [fmt.upper().lstrip('.') for fmt in self.supported_formats]
        return ", ".join(sorted(formats))


def get_file_manager(upload_dir: str = "docs") -> FileManager:
    """
    便捷函数：获取文件管理器实例

    Args:
        upload_dir: 上传文件保存目录

    Returns:
        FileManager 实例
    """
    return FileManager(upload_dir=upload_dir)
