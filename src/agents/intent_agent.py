"""
意图识别模块
用于识别用户的咨询意图类型
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class IntentType(str, Enum):
    """意图类型枚举"""
    ORDER_QUERY = "order_query"  # 订单查询
    LOGISTICS_QUERY = "logistics_query"  # 物流查询
    PRODUCT_INQUIRY = "product_inquiry"  # 商品咨询
    AFTER_SALES = "after_sales"  # 售后服务
    GENERAL_CHAT = "general_chat"  # 普通聊天
    UNKNOWN = "unknown"  # 未知意图


class IntentResult(BaseModel):
    """意图识别结果"""
    intent: IntentType = Field(default=IntentType.UNKNOWN, description="识别的意图类型")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="置信度")
    order_id: Optional[str] = Field(default=None, description="提取的订单号")
    keywords: list[str] = Field(default_factory=list, description="提取的关键词")

    def __str__(self) -> str:
        return f"意图: {self.intent.value}, 置信度: {self.confidence:.2f}, 订单号: {self.order_id}"


def match_intent(message: str) -> IntentResult:
    """
    根据用户消息匹配意图

    Args:
        message: 用户输入的消息

    Returns:
        意图识别结果
    """
    message_lower = message.lower()

    # 订单查询相关关键词
    order_keywords = ["订单", "购买记录", "买了什么", "我的订单"]
    # 物流查询相关关键词
    logistics_keywords = ["物流", "快递", "到哪了", "配送", "运输", "包裹"]
    # 商品咨询相关关键词
    product_keywords = ["商品", "产品", "价格", "多少钱", "有货吗", "库存"]
    # 售后相关关键词
    after_sales_keywords = ["退货", "换货", "退款", "售后", "保修", "维修"]

    # 计算匹配度
    order_score = sum(1 for kw in order_keywords if kw in message_lower)
    logistics_score = sum(1 for kw in logistics_keywords if kw in message_lower)
    product_score = sum(1 for kw in product_keywords if kw in message_lower)
    after_sales_score = sum(1 for kw in after_sales_keywords if kw in message_lower)

    # 提取订单号（简单匹配）
    import re
    order_id_match = re.search(r'(ORD\d+)', message)
    order_id = order_id_match.group(1) if order_id_match else None

    # 确定意图
    max_score = max(order_score, logistics_score, product_score, after_sales_score)

    if max_score == 0:
        return IntentResult(intent=IntentType.GENERAL_CHAT, confidence=0.5)

    if order_score == max_score:
        return IntentResult(
            intent=IntentType.ORDER_QUERY,
            confidence=min(order_score / 2, 1.0),
            order_id=order_id
        )
    elif logistics_score == max_score:
        return IntentResult(
            intent=IntentType.LOGISTICS_QUERY,
            confidence=min(logistics_score / 2, 1.0),
            order_id=order_id
        )
    elif product_score == max_score:
        return IntentResult(
            intent=IntentType.PRODUCT_INQUIRY,
            confidence=min(product_score / 2, 1.0)
        )
    else:
        return IntentResult(
            intent=IntentType.AFTER_SALES,
            confidence=min(after_sales_score / 2, 1.0)
        )
