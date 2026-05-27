import redis.asyncio as redis

REDIS_HOST="localhost"
REDIS_PORT=6379

#创建redis的连接对象
redis_client=redis.Redis(
    host=REDIS_HOST,#redis服务地址
    port=REDIS_PORT,
    db=0,#redis数据库编号，0-15
    decode_responses=True
)