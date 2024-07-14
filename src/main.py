from typing import Annotated, Any, AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.crud import (
    create_post,
    create_user,
    delete_post,
    get_posts,
    get_user,
    login_user,
    validate_authtoken,
)
from src.database import async_session_factory
from src.schemas.posts import PostResponseSchema, PostSchema
from src.schemas.users import UserResponseSchema, UserSchema

app = FastAPI(docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


@app.post("/v1/register", response_model=UserResponseSchema)
async def register(
    user: UserSchema, db: Annotated[AsyncSession, Depends(get_db)]
) -> Any:
    """Creates a new user."""
    user_exists = await get_user(db, user.email)
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user)
    return user


@app.post("/v1/login", response_model=UserResponseSchema)
async def login(user: UserSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> Any:
    """Logs in new users."""
    user_exists = await get_user(db, user.email)
    if not user_exists:
        raise HTTPException(status_code=404, detail="User does not exist")
    user = await login_user(db, user)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return user


@app.post("/v1/posts/create", response_model=PostResponseSchema)
async def create_posts(
    request: Request,
    post: PostSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Any:
    """Creates new post."""
    user = await validate_authtoken(db, request.headers.get("authorization"))
    if not user:
        raise HTTPException(status_code=422, detail="Invalid authorization token")

    post = await create_post(db, post, user.id)
    if not post:
        raise HTTPException(status_code=400, detail="Post already exists for this user")

    return post


@app.get("/v1/posts", response_model=list[PostResponseSchema])
async def fetch_posts(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Any:
    """Retrieves all user's posts from database."""
    user = await validate_authtoken(db, request.headers.get("authorization"))
    if not user:
        raise HTTPException(status_code=422, detail="Invalid authorization token")

    posts = await get_posts(db, user.id)
    return sorted(posts, key=lambda x: x.id)


@app.delete("/v1/posts/{todo_id}")
async def delete_posts(
    request: Request, post_id: int, db: Annotated[AsyncSession, Depends(get_db)]
) -> Any:
    """Deletes post with id from database."""
    user = await validate_authtoken(db, request.headers.get("authorization"))
    if not user:
        raise HTTPException(status_code=422, detail="Invalid authorization token")
    post = await delete_post(db, post_id, user.id)
    if not post:
        raise HTTPException(status_code=404, detail="Post instance not found")
    return "Post deleted successfully"
