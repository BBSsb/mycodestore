"""
创建示例文档目录的脚本
用于设置 RAG 系统所需的文档目录和示例文档
"""
import os
import shutil


def setup_docs():
    """设置 docs 目录并复制示例文档"""

    docs_dir = "docs"

    # 1. 创建 docs 目录
    print("创建文档目录...")
    os.makedirs(docs_dir, exist_ok=True)
    print(f"✓ 目录 '{docs_dir}' 已创建")

    # 2. 如果有测试文档，复制过来
    test_file = "test_docs/ai_intro.txt"
    if os.path.exists(test_file):
        dest_file = os.path.join(docs_dir, "ai_intro.txt")
        shutil.copy(test_file, dest_file)
        print(f"✓ 已复制 {test_file} 到 {dest_file}")
    else:
        # 3. 如果没有测试文档，创建一个示例文档
        sample_content = """人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。

人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

机器学习是人工智能的核心技术之一。它是一种让计算机通过数据来进行学习的方法。机器学习算法通过分析大量数据，自动发现数据中的规律和模式，并利用这些规律对新的数据进行预测或决策。

深度学习是机器学习的进一步发展，它使用多层神经网络来处理复杂的数据。深度学习在图像识别、语音识别、自然语言处理等领域取得了巨大的成功。

自然语言处理（NLP）是人工智能的一个重要分支，它研究如何让计算机理解和处理人类语言。NLP的应用包括机器翻译、情感分析、文本摘要、问答系统等。

计算机视觉是人工智能的另一个重要应用领域，它使计算机能够"看"和理解图像内容。计算机视觉的应用包括人脸识别、自动驾驶、医学影像分析等。"""

        dest_file = os.path.join(docs_dir, "ai_intro.txt")
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"✓ 已创建示例文档 {dest_file}")

    print("\n" + "=" * 60)
    print("文档目录设置完成！")
    print("=" * 60)
    print(f"\n你现在可以：")
    print(f"1. 将你的 PDF、TXT、DOCX、Markdown 文档放入 '{docs_dir}' 目录")
    print(f"2. 运行主程序: python main.py")
    print("=" * 60)


if __name__ == "__main__":
    setup_docs()
