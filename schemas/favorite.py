from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    """收藏状态响应模型"""
    is_favorite: bool = Field(...,alias="isFavorite", description="是否收藏")



class FavoriteaddRequest(BaseModel):
    """收藏请求模型"""
    news_id: int = Field(..., alias="newsId", description="新闻ID")

# 收藏类
class FavoriteNewsItemResponse(NewsItemBase):
    """收藏列表接口响应模型类"""
    favorite_id: int = Field(..., alias="favoriteId", description="收藏ID")
    favorite_time: datetime = Field(..., alias="favoriteTime", description="收藏时间")

#收藏列表接口响应模型类
class FavoriteListResponse(BaseModel):
    """收藏列表接口响应模型类"""
    list: list[FavoriteNewsItemResponse]
    total: int = Field(..., description="收藏列表总数")
    has_more:bool = Field(...,alias="hasMore",description="是否有更多")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )