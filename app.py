"""
RAG 系统 Streamlit Web 界面
"""
import os
import dotenv
from pathlib import Path
import streamlit as st
import shutil
import time
from document_loader.loader import load_documents
from document_loader.chunker import chunk_documents
from vector_store.vector_db import VectorDatabase
from rag_chain.rag_builder import RAGChain
from utils.file_manager import get_file_manager

dotenv.load_dotenv()


# 页面配置
st.set_page_config(
    page_title="智能文档问答系统",
    page_icon="🤖",
    layout="wide"
)


def initialize_rag_system(doc_path: str = "docs", db_path: str = "chroma_db"):
    """
    初始化 RAG 系统

    Args:
        doc_path: 文档路径
        db_path: 向量数据库路径

    Returns:
        RAGChain 实例
    """
    if not os.path.exists(doc_path):
        return None

    # 加载文档
    documents = load_documents(doc_path)
    if not documents:
        return None

    # 分割文档
    chunks = chunk_documents(documents, chunk_size=500, chunk_overlap=50)

    # 创建向量数据库
    db = VectorDatabase(persist_directory=db_path)
    db.from_documents(chunks, collection_name="rag_collection")

    # 创建 RAG 链
    rag = RAGChain(
        persist_directory=db_path,
        collection_name="rag_collection",
        model_name="qwen-plus-2025-07-28"
    )

    return rag


def safe_delete_directory(path: str, max_retries: int = 3):
    """
    安全删除目录，处理文件占用问题

    Args:
        path: 要删除的目录路径
        max_retries: 最大重试次数
    """
    if not os.path.exists(path):
        return

    for attempt in range(max_retries):
        try:
            shutil.rmtree(path)
            return
        except PermissionError as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            else:
                raise Exception(f"无法删除目录 {path}，请关闭相关程序后重试。错误: {e}")
        except Exception as e:
            raise Exception(f"删除目录失败: {e}")


def rebuild_vector_db(doc_path: str = "docs", db_path: str = "chroma_db"):
    """
    重新构建向量数据库

    Args:
        doc_path: 文档路径
        db_path: 向量数据库路径

    Returns:
        RAGChain 实例
    """
    # 删除旧的向量数据库
    if os.path.exists(db_path):
        safe_delete_directory(db_path)

    # 重新初始化
    return initialize_rag_system(doc_path, db_path)


def main():
    """主函数"""

    # 标题
    st.title("🤖 智能文档问答系统")
    st.markdown("---")

    # 初始化文件管理器
    file_manager = get_file_manager("docs")

    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 系统配置")

        # 文件上传
        st.subheader("📤 上传文档")
        uploaded_files = st.file_uploader(
            "选择文件上传",
            type=['pdf', 'txt', 'docx', 'md', 'markdown'],
            accept_multiple_files=True,
            help=f"支持 {file_manager.get_supported_formats_str()} 格式",
            key="file_uploader"
        )

        if uploaded_files:
            # 检查是否已经处理过这些文件
            if "uploaded_file_names" not in st.session_state:
                st.session_state.uploaded_file_names = []

            # 过滤掉已经上传的文件
            new_files = [f for f in uploaded_files if f.name not in st.session_state.uploaded_file_names]

            if new_files:
                with st.spinner("正在保存文件..."):
                    saved_paths = file_manager.save_multiple_files(new_files)

                if saved_paths:
                    # 记录已上传的文件名
                    for f in new_files:
                        st.session_state.uploaded_file_names.append(f.name)

                    st.success(f"✅ 成功上传 {len(saved_paths)} 个文件")
                    st.info("请点击'重新构建知识库'按钮更新索引")

                    # 重置上传组件
                    st.rerun()
            else:
                # 所有文件都已上传过，不重复处理
                pass

        # 重置上传状态的按钮
        if st.button("🔄 重置上传状态", use_container_width=True, key="reset_upload"):
            if "uploaded_file_names" in st.session_state:
                st.session_state.uploaded_file_names = []
            st.rerun()

        st.markdown("---")

        # 文档管理
        st.subheader("📁 文档管理")
        doc_count, file_names = get_document_info("docs")

        if doc_count > 0:
            st.success(f"✅ 共有 {doc_count} 个文档")

            with st.expander("查看文档列表"):
                for fname in file_names:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"• {fname}")
                    with col2:
                        if st.button("🗑️", key=f"del_{fname}", help=f"删除 {fname}"):
                            file_manager.delete_file(fname)
                            st.warning("文档已删除，请点击'重新构建知识库'更新索引")
                            st.rerun()

            # 清空所有文档按钮（二次确认机制）
            if "confirm_clear_docs" not in st.session_state:
                st.session_state.confirm_clear_docs = False

            if st.button("🗑️ 清空所有文档", use_container_width=True, key="clear_all_docs"):
                if not st.session_state.confirm_clear_docs:
                    st.session_state.confirm_clear_docs = True
                    st.rerun()
                else:
                    count = file_manager.clear_all_files()
                    st.success(f"已删除 {count} 个文件")
                    st.session_state.confirm_clear_docs = False
                    st.info("请点击'重新构建知识库'更新索引")
                    st.rerun()

            # 显示确认提示
            if st.session_state.get("confirm_clear_docs", False):
                st.warning("⚠️ **确定要删除吗？**\n\n请再次点击'清空所有文档'按钮以确认删除操作")
        else:
            st.warning("⚠️ 暂无文档")

        st.markdown("---")

        # 参数配置
        st.subheader("🔧 检索参数")
        top_k = st.slider("返回最相似的文档数量", 1, 10, 5)

        st.markdown("---")

        # 使用说明
        st.subheader("📖 使用说明")
        st.markdown("""
        1. **上传文档**：在上方选择文件上传
        2. **构建知识库**：上传后点击"重新构建知识库"
        3. **开始提问**：在下方输入框提问
        4. **查看来源**：展开回答可查看参考来源
        
        **支持的格式**：
        - PDF 文档
        - TXT 文本
        - Word 文档 (.docx)
        - Markdown 文件
        """)

    # 初始化 RAG 系统
    if "rag_initialized" not in st.session_state or "rag" not in st.session_state:
        with st.spinner("正在初始化 RAG 系统..."):
            rag = initialize_rag_system()

            if rag is None:
                st.info("👈 请先在左侧上传文档")
                st.stop()

            st.session_state.rag = rag
            st.session_state.rag_initialized = True
            st.success("✅ RAG 系统初始化完成！")

    rag = st.session_state.get('rag')

    if rag is None:
        st.error("❌ RAG 系统未正确初始化")
        st.stop()

    # 主界面
    st.subheader("💬 开始提问")

    # 聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # 如果是 AI 回复，显示来源
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 查看参考来源"):
                    for source in message["sources"]:
                        st.markdown(f"**来源 {source['index']}:**")
                        st.markdown(source["content"])
                        st.divider()

    # 输入框
    if prompt := st.chat_input("请输入你的问题..."):
        # 添加用户消息
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 回复
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                try:
                    result = rag.ask_with_sources(prompt)

                    st.markdown(result["answer"])

                    # 保存来源信息
                    sources_formatted = []
                    for source in result["sources"]:
                        sources_formatted.append({
                            "index": source["index"],
                            "content": source["content"]
                        })

                    # 添加到聊天历史
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": sources_formatted
                    })

                except Exception as e:
                    error_msg = f"❌ 错误: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

    # 底部按钮
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑️ 清空对话"):
            st.session_state.messages = []
            st.rerun()

    with col2:
        if st.button("🔄 重新加载文档"):
            st.session_state.rag_initialized = False
            if 'rag' in st.session_state:
                del st.session_state.rag
            st.rerun()

    with col3:
        if st.button("📊 系统信息"):
            doc_count = file_manager.get_file_count()
            st.info(f"""
            - 文档数量: {doc_count}
            - 模型: qwen-plus-2025-07-28
            - 向量数据库: ChromaDB
            - 嵌入模型: text-embedding-v3
            """)


def get_document_info(doc_path: str = "docs"):
    """获取文档信息"""
    if not os.path.exists(doc_path):
        return 0, []

    files = list(Path(doc_path).glob("*"))
    file_names = [f.name for f in files if f.is_file()]
    return len(files), file_names


if __name__ == "__main__":
    main()
