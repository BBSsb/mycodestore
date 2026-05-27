from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import news,users,favorite
from utils.exception_handlers import register_exception_handlers

app =FastAPI()

#注册异常处理器
register_exception_handlers(app)
#添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

#挂载路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)