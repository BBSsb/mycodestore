import os
import dotenv
from document_loader.loader import load_documents
from document_loader.chunker import chunk_documents
from vector_store.vector_db import VectorDatabase
from rag_chain.rag_builder import RAGChain

dotenv.load_dotenv()


def initialize_rag_system(doc_path: str = "docs", db_path: str = "chroma_db"):
    """
    初始化 RAG 系统

    Args:
        doc_path: 文档路径（文件或目录）
        db_path: 向量数据库路径

    Returns:
        RAGChain 实例
    """
    print("=" * 60)
    print("初始化 RAG 系统")
    print("=" * 60)

    # 1. 加载文档
    print("\n【步骤1】加载文档...")
    if not os.path.exists(doc_path):
        print(f"错误: 文档路径 '{doc_path}' 不存在")
        print("请先将文档放入该目录")
        return None

    documents = load_documents(doc_path)
    if not documents:
        print("错误: 没有加载到任何文档")
        return None

    # 2. 分割文档
    print("\n【步骤2】分割文档...")
    chunks = chunk_documents(documents, chunk_size=500, chunk_overlap=50)

    # 3. 创建向量数据库
    print("\n【步骤3】创建向量数据库...")
    db = VectorDatabase(persist_directory=db_path)
    db.from_documents(chunks, collection_name="rag_collection")

    # 4. 创建 RAG 链
    print("\n【步骤4】创建 RAG 链...")
    rag = RAGChain(
        persist_directory=db_path,
        collection_name="rag_collection",
        model_name="qwen-plus-2025-07-28"
    )

    print("\n" + "=" * 60)
    print("RAG 系统初始化完成！")
    print("=" * 60)

    return rag


def interactive_chat(rag: RAGChain):
    """
    交互式聊天模式

    Args:
        rag: RAGChain 实例
    """
    print("\n进入交互问答模式（输入 'quit' 或 'exit' 退出）")
    print("-" * 60)

    while True:
        question = input("\n请输入你的问题: ").strip()

        if question.lower() in ['quit', 'exit', '退出']:
            print("再见！")
            break

        if not question:
            continue

        try:
            result = rag.ask_with_sources(question)

            print("\n" + "=" * 60)
            print(f"问题: {result['question']}")
            print(f"\n回答: {result['answer']}")
            print("\n参考来源:")
            for source in result['sources']:
                print(f"  [{source['index']}] {source['content'][:100]}...")
            print("=" * 60)

        except Exception as e:
            print(f"\n错误: {e}")


def main():
    """主函数"""

    # 配置路径
    DOC_PATH = "docs"  # 文档目录
    DB_PATH = "chroma_db"  # 向量数据库目录

    # 初始化 RAG 系统
    rag = initialize_rag_system(doc_path=DOC_PATH, db_path=DB_PATH)

    if rag is None:
        print("\nRAG 系统初始化失败")
        return

    # 启动交互式聊天
    interactive_chat(rag)


if __name__ == "__main__":
    main()
