"""
文档处理测试脚本
"""
import os
from document_loader.loader import load_documents
from document_loader.chunker import chunk_documents


def test_document_processing():
    """测试文档处理流程"""

    # 1. 创建测试文档目录
    test_dir = "test_docs"
    os.makedirs(test_dir, exist_ok=True)

    # 2. 创建示例文本文件
    sample_text = """
    人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。

    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

    人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

    机器学习是人工智能的核心技术之一。它是一种让计算机通过数据来进行学习的方法。机器学习算法通过分析大量数据，自动发现数据中的规律和模式，并利用这些规律对新的数据进行预测或决策。

    深度学习是机器学习的进一步发展，它使用多层神经网络来处理复杂的数据。深度学习在图像识别、语音识别、自然语言处理等领域取得了巨大的成功。
    """

    sample_file = os.path.join(test_dir, "ai_intro.txt")
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_text)

    print("=" * 50)
    print("开始测试文档处理流程")
    print("=" * 50)

    # 3. 加载文档
    print("\n【步骤1】加载文档...")
    documents = load_documents(test_dir)
    print(f"加载了 {len(documents)} 个文档")

    if not documents:
        print("错误：没有加载到任何文档")
        return

    # 4. 查看文档信息
    print("\n【步骤2】文档信息:")
    for i, doc in enumerate(documents):
        print(f"  文档 {i + 1}:")
        print(f"    内容长度: {len(doc.page_content)} 字符")
        print(f"    元数据: {doc.metadata}")

    # 5. 分割文档
    print("\n【步骤3】分割文档...")
    chunks = chunk_documents(documents, chunk_size=200, chunk_overlap=30)
    print(f"分割后得到 {len(chunks)} 个文本块")

    # 6. 查看文本块信息
    print("\n【步骤4】文本块信息:")
    for i, chunk in enumerate(chunks[:5]):  # 只显示前5个
        print(f"\n  文本块 {i + 1}:")
        print(f"    内容长度: {len(chunk.page_content)} 字符")
        print(f"    内容预览: {chunk.page_content[:100]}...")
        print(f"    元数据: {chunk.metadata}")

    print("\n" + "=" * 50)
    print("文档处理测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    test_document_processing()
