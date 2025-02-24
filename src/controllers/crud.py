from pydantic import EmailStr
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.hasher import Hasher
from src.models import Post, User
from src.schemas import PostSchema, UserSchema


async def create_user(db: AsyncSession, user: UserSchema):
    hashed_pwd = Hasher.get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_pwd)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, email: EmailStr):
    statement = select(User).where(User.email == email)
    return await db.scalar(statement)


async def login_user(db: AsyncSession, user: UserSchema):
    prev_user = await get_user(db, user.email)
    pwd_match = Hasher.verify_password(user.password, prev_user.password)
    if not pwd_match:
        return False
    return prev_user


async def create_post(db: AsyncSession, post: PostSchema, user_id: int):
    post_exists = await get_post(
        db, post_title=post.title, user_id=user_id, action="create"
    )
    if post_exists:
        return False
    post_instance = post(text=post.text, title=post.title, user_id=user_id)
    db.add(post_instance)
    await db.commit()
    await db.refresh(post_instance)
    return post_instance


async def get_post(
    db: AsyncSession,
    post_id: int = None,
    post_title: str = None,
    user_id: int = None,
    action: str = None,
):
    if action == "create":
        statement = select(Post).where(
            and_(Post.title == post_title, Post.user_id == user_id)
        )
    elif action == "delete":
        statement = select(Post).where(
            and_(Post.user_id == user_id, Post.id == post_id)
        )
    return await db.scalar(statement)


async def get_posts(db: AsyncSession, user_id: int):
    statement = select(Post).where(Post.user_id == user_id)
    return await db.scalars(statement)


async def delete_post(db: AsyncSession, post_id: int, user_id: int):
    post = await get_post(db, post_id=post_id, user_id=user_id, action="delete")
    if not post:
        return False
    await db.delete(post)
    await db.commit()
    return True


async def validate_authtoken(db: AsyncSession, authtoken: str):
    statement = select(User).where(User.auth_token == authtoken)
    return await db.scalar(statement)
