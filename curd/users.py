from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update

from config.db_conf import get_db
from models.users import User, UserToken
from schemas.users import UserRequest, UpdateUserRequest,UserChangerPasswordRequest
from utils import security
import uuid


# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    print(f"密码类型: {type(user_data.password)}")
    print(f"密码长度: {len(str(user_data.password))}")
    print(f"密码内容: {user_data.password}")
    # 先密码加密处理
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# 生成Token
async def creare_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token


# 认证用户
async def authenticate_user(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, username)

    if not user:
        return None

    # 校验密码
    if not security.verify_password(password, user.password):
        return None

    return user


# 根据token查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 更新用户信息
async def update_user(db: AsyncSession, username: str, user_data: UpdateUserRequest):
    # **把pydantic类型转换成字典，相当于解包
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result = await db.execute(query)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    updated_user = await get_user_by_username(db, username)
    return updated_user

#修改密码
async def change_password(user:  User, password_data: UserChangerPasswordRequest, db: AsyncSession):
    #验证旧密码
    if not security.verify_password(password_data.old_password, user.password):
        return False

    hash_new_pwd=security.get_hash_password(password_data.new_password)

    user.password=hash_new_pwd
    #更新用户,确保可以commit
    db.add( user)
    await db.commit()
    await db.refresh(user)
    return True
