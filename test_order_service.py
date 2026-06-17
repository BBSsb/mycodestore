# 测试订单查询
from src.services.order_service import query_order, get_order_status

# 查询存在的订单
order = query_order("ORD202601001")
print(f"订单号: {order.order_id}")
print(f"状态: {order.status}")
print(f"总金额: {order.total_amount}")
print(f"商品列表: {[item.product_name for item in order.items]}")

# 查询不存在的订单
order_none = query_order("ORD999999")
print(f"不存在的订单: {order_none}")

# 获取订单状态
status = get_order_status("ORD202601002")
print(f"订单状态: {status}")
