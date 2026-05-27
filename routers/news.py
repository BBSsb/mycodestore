
from fastapi import APIRouter, Depends, Query,HTTPException
from typing_inspection.typing_objects import alias

from curd import news
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# 创建api实例
router = APIRouter(prefix="/api/news", tags=["news"])


# 1.模块化路由——》参考API接口规范文档
# 2.定义模型类——》参考数据库表或者数据设计文档
# 3.在crud文件夹里封装操作数据的方法
# 4.在路由处理函数里面调用crud方法

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": categories
    }


@router.get("/list")
async def get_news_list(category_id: int = Query(..., alias="categoryId"),
                        page: int = 1,
                        page_size: int = Query(10, alias="pageSize"),
                        db: AsyncSession = Depends(get_db)):
    # 思路：处理分页规则
    offset = (page - 1) * page_size

    # 查询新闻列表
    new_list = await news.get_news_list(db, category_id, offset, page_size)

    # 计算总量
    total = await news.get_news_count(db, category_id)
    # 计算是否还有更多
    has_more = total > (offset + len(new_list))
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": new_list,
            "total": total,
            "hasMore": has_more
        }
    }

@router.get("/detail")
async def get_news_detail(id: int=Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    news_detail = await news.get_news_detail(db, id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

#调用增加浏览量的方法
    view_res=await news.increase_news_views(db, id)
    if not view_res:
        raise HTTPException(status_code=404, detail="增加浏览量失败")

    related_news=await news.get_related_news(db, id, news_detail.category_id)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }