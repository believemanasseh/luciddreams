from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
async_session_factory = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
