"""
物流服务模块
模拟物流查询接口
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LogisticsTrack(BaseModel):
    """物流轨迹"""
    time: datetime = Field(description="时间")
    location: str = Field(description="位置")
    description: str = Field(description="描述")


class LogisticsInfo(BaseModel):
    """物流信息"""
    order_id: str = Field(description="订单号")
    company: str = Field(description="物流公司")
    tracking_number: str = Field(description="运单号")
    status: str = Field(description="物流状态")
    tracks: list[LogisticsTrack] = Field(description="物流轨迹")


# 模拟物流数据库
MOCK_LOGISTICS = {
    "ORD202601001": LogisticsInfo(
        order_id="ORD202601001",
        company="顺丰速运",
        tracking_number="SF1234567890",
        status="运输中",
        tracks=[
            LogisticsTrack(
                time=datetime(2026, 1, 15, 11, 0),
                location="北京分拣中心",
                description="已揽收"
            ),
            LogisticsTrack(
                time=datetime(2026, 1, 15, 18, 30),
                location="北京转运中心",
                description="已发出"
            ),
            LogisticsTrack(
                time=datetime(2026, 1, 16, 8, 20),
                location="上海转运中心",
                description="已到达"
            ),
        ]
    ),
    "ORD202601002": LogisticsInfo(
        order_id="ORD202601002",
        company="京东物流",
        tracking_number="JD9876543210",
        status="派送中",
        tracks=[
            LogisticsTrack(
                time=datetime(2026, 1, 16, 15, 0),
                location="上海仓库",
                description="已出库"
            ),
            LogisticsTrack(
                time=datetime(2026, 1, 17, 9, 30),
                location="上海浦东配送站",
                description="已到达配送站"
            ),
            LogisticsTrack(
                time=datetime(2026, 1, 17, 10, 15),
                location="上海浦东配送站",
                description="快递员正在派送"
            ),
        ]
    ),
    "ORD202601003": LogisticsInfo(
        order_id="ORD202601003",
        company="中通快递",
        tracking_number="ZT1122334455",
        status="已签收",
        tracks=[
            LogisticsTrack(
                time=datetime(2026, 1, 10, 10, 0),
                location="广州分拣中心",
                description="已揽收"
            ),
            LogisticsTrack(
                time=datetime(2026, 1, 11, 14, 20),
                location="深圳转运中心",
                description="运输中"
            ),
            LogisticsTrack(
                time=datetime(2026, 1, 12, 9, 30),
                location="深圳福田配送站",
                description="派送中"
            ),
            LogisticsTrack(
                time=datetime(2026, 1, 12, 15, 45),
                location="深圳福田区",
                description="已签收，签收人：本人"
            ),
        ]
    ),
}


def query_logistics(order_id: str) -> Optional[LogisticsInfo]:
    """
    查询物流信息

    Args:
        order_id: 订单号

    Returns:
        物流信息，如果不存在返回None
    """
    return MOCK_LOGISTICS.get(order_id)


def get_logistics_status(order_id: str) -> Optional[str]:
    """
    获取物流状态

    Args:
        order_id: 订单号

    Returns:
        物流状态，如果不存在返回None
    """
    logistics = query_logistics(order_id)
    return logistics.status if logistics else None
