"""
向量数据库测试脚本
"""
import os
import dotenv
from document_loader.loader import load_documents
from document_loader.chunker import chunk_documents
from vector_store.vector_db import VectorDatabase

dotenv.load_dotenv()

def test_vector_database():
    """测试向量数据库流程"""

    print("=" * 60)
    print("开始测试向量数据库")
    print("=" * 60)

    # 1. 准备测试数据
    test_dir = "test_docs"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

        sample_text = """人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。

人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

机器学习是人工智能的核心技术之一。它是一种让计算机通过数据来进行学习的方法。机器学习算法通过分析大量数据，自动发现数据中的规律和模式，并利用这些规律对新的数据进行预测或决策。

深度学习是机器学习的进一步发展，它使用多层神经网络来处理复杂的数据。深度学习在图像识别、语音识别、自然语言处理等领域取得了巨大的成功。

自然语言处理（NLP）是人工智能的一个重要分支，它研究如何让计算机理解和处理人类语言。NLP的应用包括机器翻译、情感分析、文本摘要、问答系统等。"""

        with open(os.path.join(test_dir, "ai_intro.txt"), 'w', encoding='utf-8') as f:
            f.write(sample_text)

    # 2. 加载和分割文档
    print("\n【步骤1】加载文档...")
    documents = load_documents(test_dir)

    if not documents:
        print("错误：没有加载到任何文档")
        return

    print("\n【步骤2】分割文档...")
    chunks = chunk_documents(documents, chunk_size=200, chunk_overlap=30)

    # 3. 创建向量数据库
    print("\n【步骤3】创建向量数据库...")
    db = VectorDatabase(persist_directory="test_chroma_db")
    vector_store = db.from_documents(chunks, collection_name="test_collection")

    # 4. 搜索测试
    print("\n【步骤4】测试搜索功能...")
    queries = [
        "什么是人工智能？",
        "机器学习是什么？",
        "深度学习的应用有哪些？"
    ]

    for query in queries:
        print(f"\n  查询: {query}")
        results = db.search(query, k=3)
        print(f"  找到 {len(results)} 个结果:")
        for i, doc in enumerate(results, 1):
            print(f"    结果 {i}:")
            print(f"      内容: {doc.page_content[:80]}...")
            print(f"      来源: {doc.metadata.get('source', '未知')}")

    # 5. 测试带分数的搜索
    print("\n【步骤5】测试带分数的搜索...")
    query = "自然语言处理是什么？"
    print(f"  查询: {query}")
    results_with_scores = db.search_with_score(query, k=3)
    print(f"  找到 {len(results_with_scores)} 个结果:")
    for i, (doc, score) in enumerate(results_with_scores, 1):
        print(f"    结果 {i}:")
        print(f"      内容: {doc.page_content[:80]}...")
        print(f"      相似度分数: {score:.4f} (越低越相似)")
    
    print("\n" + "=" * 60)
    print("向量数据库测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_vector_database()
