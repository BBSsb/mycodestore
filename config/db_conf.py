from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

#数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:root@localhost:3306/news_app?charset=utf8mb4"

# 创建异步引擎
async_engine= create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    pool_recycle=20
)

# 创建异步会话工厂
AsyncSessionLocal=async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 依赖项，用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()