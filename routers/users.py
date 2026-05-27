
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from curd import users
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UpdateUserRequest,UserChangerPasswordRequest

from config.db_conf import get_db
from utils.response import success_response
from utils.auth import get_current_user
router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    #验证用户是否存在
    exist_user=await users.get_user_by_username(db, user_data.username)
    if exist_user:
        raise HTTPException(status_code=400, detail="用户已存在")

    #创建用户
    user = await users.create_user(db, user_data)

    #生成token
    token= await users.creare_token(db, user.id)

    #
    respinse_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=respinse_data)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user=await users.authenticate_user(user_data.username, user_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token= await users.creare_token(db, user.id)
    respinse_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=respinse_data)


#获取用户信息
@router.get("/info")
async def get_user_info(user:User=Depends(get_current_user)):
    #model_validate用于将任意对象转换为 Pydantic 模型实例。
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

#修改用户信息
@router.put("/update")
async def update_user_info(user_data:UpdateUserRequest,user:User=Depends(get_current_user),
                           db:AsyncSession=Depends(get_db)):
    user=await users.update_user(db,user.username,user_data)
    return success_response(message="修改用户信息成功",data=UserInfoResponse.model_validate(user))

#修改用户密码
@router.put("/password")
async def update_password(
        password_data:UserChangerPasswordRequest,
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)):
    res_change_pwd=await users.change_password(user,password_data,db)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="修改密码失败")
    return success_response(message="修改密码成功")



