
from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from curd import favorite
from config.db_conf import get_db
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteaddRequest, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response
from starlette import status
router = APIRouter(prefix="/api/favorite", tags=["favorite"])


# 判断是否收藏
@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    is_favourite = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="获取收藏状态成功", data=FavoriteCheckResponse(is_favourite=is_favourite))


# 添加收藏
@router.post("/add")
async def add_favorite(data: FavoriteaddRequest,
                       user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)


# 取消收藏
@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result=await favorite.remove_news_favorite(db,user.id,news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="收藏的记录不存在")

    return success_response(message="取消收藏成功")

@router.get("/list")
async def get_favorite_list(
        page:int =Query(1,ge=1),
        page_size:int= Query(10,ge=1,le=100,alias="pageSize"),
        user:User =Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    rows,total=await favorite.get_favorite_list(db,user.id,page,page_size)
    favorite_list=[{
        **news.__dict__,
        "favorite_time":favorite_time,
        "favorite_id":favorite_id
    }for news,favorite_time,favorite_id in rows]
    has_more=total>page *page_size

    data=FavoriteListResponse(List=favorite_list,total=total,hasMore=has_more)
    return success_response(message="获取列表成功",data=data)

@router.delete("/clear")
async def clear_favorite(
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    count =await favorite.remove_all_favorite(db,user.id)
    return success_response(message=f"清空了{count}条记录")
