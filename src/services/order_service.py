
"""
订单服务模块
模拟订单查询接口
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    """订单项"""
    product_name: str = Field(description="商品名称")
    quantity: int = Field(description="数量")
    price: float = Field(description="单价")


class OrderInfo(BaseModel):
    """订单信息"""
    order_id: str = Field(description="订单号")
    status: str = Field(description="订单状态")
    create_time: datetime = Field(description="创建时间")
    total_amount: float = Field(description="总金额")
    items: list[OrderItem] = Field(description="商品列表")
    receiver: str = Field(description="收货人")
    address: str = Field(description="收货地址")
    phone: str = Field(description="联系电话")


# 模拟订单数据库
MOCK_ORDERS = {
    "ORD202601001": OrderInfo(
        order_id="ORD202601001",
        status="已发货",
        create_time=datetime(2026, 1, 15, 10, 30),
        total_amount=299.99,
        items=[
            OrderItem(product_name="Python编程从入门到精通", quantity=1, price=89.99),
            OrderItem(product_name="JavaScript高级程序设计", quantity=1, price=210.00),
        ],
        receiver="张三",
        address="北京市朝阳区xxx街道xxx号",
        phone="138****1234"
    ),
    "ORD202601002": OrderInfo(
        order_id="ORD202601002",
        status="配送中",
        create_time=datetime(2026, 1, 16, 14, 20),
        total_amount=599.00,
        items=[
            OrderItem(product_name="机械键盘", quantity=1, price=599.00),
        ],
        receiver="李四",
        address="上海市浦东新区xxx路xxx号",
        phone="139****5678"
    ),
    "ORD202601003": OrderInfo(
        order_id="ORD202601003",
        status="已完成",
        create_time=datetime(2026, 1, 10, 9, 15),
        total_amount=1599.00,
        items=[
            OrderItem(product_name="无线鼠标", quantity=2, price=199.50),
            OrderItem(product_name="显示器支架", quantity=1, price=1200.00),
        ],
        receiver="王五",
        address="广州市天河区xxx大道xxx号",
        phone="136****9012"
    ),
}


def query_order(order_id: str) -> Optional[OrderInfo]:
    """
    查询订单信息

    Args:
        order_id: 订单号

    Returns:
        订单信息，如果不存在返回None
    """
    return MOCK_ORDERS.get(order_id)


def get_order_status(order_id: str) -> Optional[str]:
    """
    获取订单状态

    Args:
        order_id: 订单号

    Returns:
        订单状态，如果不存在返回None
    """
    order = query_order(order_id)
    return order.status if order else None
