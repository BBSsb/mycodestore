# NEW_FILE_CODE
"""
电商智能客服Streamlit前端应用
"""

import streamlit as st
from src.agents.workflow import process_user_message


def main():
    """主函数"""
    st.set_page_config(
        page_title="电商智能客服",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 电商智能客服助手")
    st.markdown("---")

    # 初始化session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示欢迎消息
    if not st.session_state.messages:
        welcome_msg = process_user_message("你好")
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 聊天输入框
    if prompt := st.chat_input("请输入您的问题..."):
        # 添加用户消息到历史
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            # 显示加载状态
            with st.spinner("正在思考中..."):
                try:
                    response = process_user_message(prompt)
                except Exception as e:
                    response = f"❌ 发生错误: {str(e)}"

            st.write(response)
            # 添加助手回复到历史
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
