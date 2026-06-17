"""
电商客服多Agent工作流
基于LangGraph构建
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.types import TypedDict

from src.agents.intent_agent import IntentResult, IntentType, match_intent
from src.services.order_service import query_order, OrderInfo
from src.services.logistics_service import query_logistics, LogisticsInfo
from src.utils.formatters import format_order_response, format_logistics_response
from src.config.llm_config import get_llm_client, LLMConfig


# 定义状态
class AgentState(TypedDict):
    """Agent状态"""
    messages: list  # 对话消息历史
    intent: IntentResult  # 意图识别结果
    order_info: OrderInfo | None  # 订单信息
    logistics_info: LogisticsInfo | None  # 物流信息
    response: str  # 最终回复


def intent_recognition_node(state: AgentState) -> dict:
    """
    意图识别节点
    分析用户消息，识别意图类型
    """
    user_message = state["messages"][-1]

    # 如果是字符串，直接使用；如果是字典，提取content
    if isinstance(user_message, str):
        message_text = user_message
    else:
        message_text = user_message.get("content", "") if isinstance(user_message, dict) else str(user_message)

    # 尝试使用LLM进行意图识别
    llm = get_llm_client()

    if llm:
        intent_result = llm_based_intent_recognition(llm, message_text)
    else:
        # 降级到规则匹配
        intent_result = match_intent(message_text)

    print(f"[意图识别] 识别结果: {intent_result}")

    return {
        "intent": intent_result
    }


def llm_based_intent_recognition(llm, message: str) -> IntentResult:
    """
    基于LLM的意图识别

    Args:
        llm: LLM实例
        message: 用户消息

    Returns:
        意图识别结果
    """
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_template("""你是一个电商客服意图识别专家。请分析用户的消息，识别其意图类型。

支持的意图类型：
- order_query: 订单查询（询问订单状态、订单详情等）
- logistics_query: 物流查询（询问快递进度、包裹位置等）
- product_inquiry: 商品咨询（询问商品信息、价格、库存等）
- after_sales: 售后服务（退货、换货、退款、保修等）
- general_chat: 普通聊天（问候、闲聊等）

用户消息：{message}

请只返回JSON格式的结果，包含以下字段：
- intent: 意图类型（从上面选择一个）
- confidence: 置信度（0-1之间的浮点数）
- order_id: 如果提到订单号，提取出来（格式如ORD202601001），否则为null

只返回JSON，不要其他内容。""")

    try:
        response = llm.invoke(prompt.format(message=message))
        content = response.content.strip()

        # 解析JSON响应
        import json
        import re

        # 提取JSON部分
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return IntentResult(
                intent=IntentType(result.get("intent", "unknown")),
                confidence=result.get("confidence", 0.5),
                order_id=result.get("order_id")
            )
    except Exception as e:
        print(f"LLM意图识别失败: {e}，降级到规则匹配")

    # 失败时降级到规则匹配
    return match_intent(message)


def order_query_node(state: AgentState) -> dict:
    """
    订单查询节点
    根据订单号查询订单信息
    """
    intent = state["intent"]
    order_id = intent.order_id

    if not order_id:
        return {
            "response": "请提供您要查询的订单号，例如：ORD202601001"
        }

    order_info = query_order(order_id)

    if order_info:
        response = format_order_response(order_info)
        return {
            "order_info": order_info,
            "response": response
        }
    else:
        return {
            "response": f"❌ 抱歉，未找到订单号为 {order_id} 的订单信息，请检查订单号是否正确。"
        }


def logistics_query_node(state: AgentState) -> dict:
    """
    物流查询节点
    根据订单号查询物流信息
    """
    intent = state["intent"]
    order_id = intent.order_id

    if not order_id:
        return {
            "response": "请提供您要查询物流的订单号，例如：ORD202601001"
        }

    logistics_info = query_logistics(order_id)

    if logistics_info:
        response = format_logistics_response(logistics_info)
        return {
            "logistics_info": logistics_info,
            "response": response
        }
    else:
        return {
            "response": f"❌ 抱歉，未找到订单号为 {order_id} 的物流信息，请检查订单号是否正确。"
        }


def product_inquiry_node(state: AgentState) -> dict:
    """
    商品咨询节点
    处理商品相关咨询
    """
    llm = get_llm_client()

    if llm:
        try:
            from langchain_core.prompts import ChatPromptTemplate

            prompt = ChatPromptTemplate.from_template("""你是一个专业的电商客服。用户正在咨询商品信息。

可用的商品信息：
1. Python编程从入门到精通 - ¥89.99
2. JavaScript高级程序设计 - ¥210.00
3. 机械键盘 - ¥599.00
4. 无线鼠标 - ¥199.50
5. 显示器支架 - ¥1200.00

用户问题：{message}

请友好、专业地回答用户的问题。如果问到具体价格或库存，请根据上面的信息回答。保持回复简洁明了。""")

            user_message = state["messages"][-1]
            if isinstance(user_message, dict):
                user_message = user_message.get("content", "")

            response = llm.invoke(prompt.format(message=user_message))
            return {"response": response.content}
        except Exception as e:
            print(f"LLM商品咨询失败: {e}，使用默认回复")

    return {
        "response": "📝 关于商品咨询，您可以询问商品价格、库存、规格等信息。目前我们支持以下商品：\n- Python编程从入门到精通\n- JavaScript高级程序设计\n- 机械键盘\n- 无线鼠标\n- 显示器支架\n\n请问您想了解哪个商品的详细信息？"
    }


def after_sales_node(state: AgentState) -> dict:
    """
    售后服务节点
    处理售后相关问题
    """
    llm = get_llm_client()

    if llm:
        try:
            from langchain_core.prompts import ChatPromptTemplate

            prompt = ChatPromptTemplate.from_template("""你是一个专业的电商客服售后专员。用户正在咨询售后问题。

售后政策：
- 7天无理由退货
- 15天内可换货
- 所有商品享受1年质保
- 退款申请后1-3个工作日处理

用户问题：{message}

请友好、耐心地回答用户的问题，并提供具体的操作指引。如果用户提供了订单号，可以建议他们先查询订单状态。""")

            user_message = state["messages"][-1]
            if isinstance(user_message, dict):
                user_message = user_message.get("content", "")

            response = llm.invoke(prompt.format(message=user_message))
            return {"response": response.content}
        except Exception as e:
            print(f"LLM售后咨询失败: {e}，使用默认回复")

    return {
        "response": "🔧 关于售后服务：\n\n1️⃣ **退货政策**：7天无理由退货\n2️⃣ **换货政策**：15天内可换货\n3️⃣ **保修政策**：所有商品享受1年质保\n4️⃣ **退款流程**：申请后1-3个工作日处理\n\n如需办理售后，请提供订单号，我会为您查询具体订单的售后状态。"
    }


def general_chat_node(state: AgentState) -> dict:
    """
    普通聊天节点
    处理日常对话
    """
    llm = get_llm_client()

    if llm:
        try:
            from langchain_core.prompts import ChatPromptTemplate

            prompt = ChatPromptTemplate.from_template("""你是一个友好的电商客服助手。用户正在和你聊天。

你可以提供的服务包括：
- 📦 订单查询
- 🚚 物流查询
- 📝 商品咨询
- 🔧 售后服务

用户消息：{message}

请友好地回应用户，并引导用户提出具体的需求。保持回复简洁、亲切，可以使用一些表情符号让对话更生动。""")

            user_message = state["messages"][-1]
            if isinstance(user_message, dict):
                user_message = user_message.get("content", "")

            response = llm.invoke(prompt.format(message=user_message))
            return {"response": response.content}
        except Exception as e:
            print(f"LLM聊天失败: {e}，使用默认回复")

    return {
        "response": "👋 您好！我是电商智能客服助手，可以为您提供以下服务：\n\n📦 **订单查询** - 查询订单状态和详情\n🚚 **物流查询** - 查看物流配送进度\n📝 **商品咨询** - 了解商品信息和价格\n🔧 **售后服务** - 退换货和保修咨询\n\n请问有什么可以帮您的吗？"
    }


def route_by_intent(state: AgentState) -> Literal[
    "order_query",
    "logistics_query",
    "product_inquiry",
    "after_sales",
    "general_chat"
]:
    """
    根据意图路由到不同的处理节点
    """
    intent_type = state["intent"].intent

    route_map = {
        IntentType.ORDER_QUERY: "order_query",
        IntentType.LOGISTICS_QUERY: "logistics_query",
        IntentType.PRODUCT_INQUIRY: "product_inquiry",
        IntentType.AFTER_SALES: "after_sales",
        IntentType.GENERAL_CHAT: "general_chat",
    }

    next_node = route_map.get(intent_type, "general_chat")
    print(f"[路由决策] 跳转到节点: {next_node}")

    return next_node


def create_customer_service_graph():
    """
    创建客服工作流图

    Returns:
        编译后的工作流图
    """
    # 创建工作流图
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("intent_recognition", intent_recognition_node)
    workflow.add_node("order_query", order_query_node)
    workflow.add_node("logistics_query", logistics_query_node)
    workflow.add_node("product_inquiry", product_inquiry_node)
    workflow.add_node("after_sales", after_sales_node)
    workflow.add_node("general_chat", general_chat_node)

    # 设置入口点
    workflow.set_entry_point("intent_recognition")

    # 添加条件边（路由）
    workflow.add_conditional_edges(
        source="intent_recognition",
        path=route_by_intent,
        path_map={
            "order_query": "order_query",
            "logistics_query": "logistics_query",
            "product_inquiry": "product_inquiry",
            "after_sales": "after_sales",
            "general_chat": "general_chat",
        }
    )

    # 所有处理节点都连接到END
    workflow.add_edge("order_query", END)
    workflow.add_edge("logistics_query", END)
    workflow.add_edge("product_inquiry", END)
    workflow.add_edge("after_sales", END)
    workflow.add_edge("general_chat", END)

    # 编译工作流
    app = workflow.compile()

    return app


# 创建全局实例
customer_service_app = create_customer_service_graph()


def process_user_message(message: str) -> str:
    """
    处理用户消息的主函数

    Args:
        message: 用户输入的消息

    Returns:
        客服回复
    """
    # 初始化状态
    initial_state = {
        "messages": [message],
        "intent": None,
        "order_info": None,
        "logistics_info": None,
        "response": ""
    }

    # 运行工作流
    result = customer_service_app.invoke(initial_state)

    return result["response"]
