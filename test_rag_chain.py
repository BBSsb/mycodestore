"""
RAG 链测试脚本
"""
import os
import shutil
import dotenv
from document_loader.loader import load_documents
from document_loader.chunker import chunk_documents
from vector_store.vector_db import VectorDatabase
from rag_chain.rag_builder import RAGChain

dotenv.load_dotenv()


def test_rag_chain():
    """测试 RAG 链功能"""

    print("=" * 60)
    print("开始测试 RAG 链")
    print("=" * 60)

    # 1. 准备数据（强制重新创建）
    test_dir = "test_docs"
    db_dir = "rag_chroma_db"

    # 清理旧数据
    if os.path.exists(db_dir):
        print("\n清理旧的向量数据库...")
        shutil.rmtree(db_dir)

    os.makedirs(test_dir, exist_ok=True)

    sample_text = """人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。

人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

机器学习是人工智能的核心技术之一。它是一种让计算机通过数据来进行学习的方法。机器学习算法通过分析大量数据，自动发现数据中的规律和模式，并利用这些规律对新的数据进行预测或决策。

深度学习是机器学习的进一步发展，它使用多层神经网络来处理复杂的数据。深度学习在图像识别、语音识别、自然语言处理等领域取得了巨大的成功。

自然语言处理（NLP）是人工智能的一个重要分支，它研究如何让计算机理解和处理人类语言。NLP的应用包括机器翻译、情感分析、文本摘要、问答系统等。

计算机视觉是人工智能的另一个重要应用领域，它使计算机能够"看"和理解图像内容。计算机视觉的应用包括人脸识别、自动驾驶、医学影像分析等。"""

    with open(os.path.join(test_dir, "ai_intro.txt"), 'w', encoding='utf-8') as f:
        f.write(sample_text)

    print("\n【步骤1】准备数据...")
    documents = load_documents(test_dir)
    chunks = chunk_documents(documents, chunk_size=200, chunk_overlap=30)

    print("\n【步骤2】创建向量数据库...")
    db = VectorDatabase(persist_directory=db_dir)
    db.from_documents(chunks, collection_name="rag_collection")

    # 2. 创建 RAG 链
    print("\n【步骤3】创建 RAG 链...")
    rag = RAGChain(
        persist_directory=db_dir,
        collection_name="rag_collection",
        model_name="qwen-plus-2025-07-28"
    )

    # 3. 测试问答
    print("\n【步骤4】测试问答功能...")
    questions = [
        "什么是人工智能？",
        "机器学习有哪些应用？",
        "深度学习和机器学习有什么关系？",
        "自然语言处理的应用场景有哪些？"
    ]

    for question in questions:
        print("\n" + "-" * 60)
        answer = rag.ask(question)

    # 4. 测试带来源的问答
    print("\n" + "=" * 60)
    print("【步骤5】测试带来源的问答...")
    print("-" * 60)
    question = "计算机视觉是什么？"
    result = rag.ask_with_sources(question)

    print("\n详细来源信息:")
    for source in result["sources"]:
        print(f"\n  来源 {source['index']}:")
        print(f"    内容: {source['content']}...")
        print(f"    元数据: {source['metadata']}")

    print("\n" + "=" * 60)
    print("RAG 链测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_rag_chain()
