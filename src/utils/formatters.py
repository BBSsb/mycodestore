# NEW_FILE_CODE
"""
格式化工具模块
用于格式化订单和物流信息的输出
"""

from src.services.order_service import OrderInfo
from src.services.logistics_service import LogisticsInfo


def format_order_response(order: OrderInfo) -> str:
    """
    格式化订单信息回复

    Args:
        order: 订单信息对象

    Returns:
        格式化后的订单信息字符串
    """
    items_text = "\n".join([
        f"  - {item.product_name} x{item.quantity} ¥{item.price:.2f}"
        for item in order.items
    ])

    response = f"""
📦 **订单信息**

订单号：{order.order_id}
订单状态：{order.status}
下单时间：{order.create_time.strftime('%Y-%m-%d %H:%M')}
收货人：{order.receiver}
联系电话：{order.phone}
收货地址：{order.address}

**商品列表：**
{items_text}

**订单总额：** ¥{order.total_amount:.2f}
    """.strip()

    return response


def format_logistics_response(logistics: LogisticsInfo) -> str:
    """
    格式化物流信息回复

    Args:
        logistics: 物流信息对象

    Returns:
        格式化后的物流信息字符串
    """
    tracks_text = "\n".join([
        f"  - {track.time.strftime('%m-%d %H:%M')} {track.location}\n    {track.description}"
        for track in logistics.tracks
    ])

    response = f"""
🚚 **物流信息**

订单号：{logistics.order_id}
物流公司：{logistics.company}
运单号：{logistics.tracking_number}
当前状态：{logistics.status}

**物流轨迹：**
{tracks_text}
    """.strip()

    return response


def format_error_response(message: str) -> str:
    """
    格式化错误信息回复

    Args:
        message: 错误消息

    Returns:
        格式化后的错误信息字符串
    """
    return f"❌ {message}"


def format_success_response(message: str) -> str:
    """
    格式化成功信息回复

    Args:
        message: 成功消息

    Returns:
        格式化后的成功信息字符串
    """
    return f"✅ {message}"
