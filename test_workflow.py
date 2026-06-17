# 测试工作流
from src.agents.workflow import process_user_message

# 测试1: 订单查询
print("=" * 50)
print("测试1: 订单查询")
print("=" * 50)
response = process_user_message("我想查一下订单ORD202601001")
print(response)
print()

# 测试2: 物流查询
print("=" * 50)
print("测试2: 物流查询")
print("=" * 50)
response = process_user_message("帮我查查ORD202601002的物流")
print(response)
print()

# 测试3: 普通聊天
print("=" * 50)
print("测试3: 普通聊天")
print("=" * 50)
response = process_user_message("你好")
print(response)
print()

# 测试4: 商品咨询
print("=" * 50)
print("测试4: 商品咨询")
print("=" * 50)
response = process_user_message("这个商品多少钱？")
print(response)
