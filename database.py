"""
DB 설정 (Database Layer)
- 비동기 엔진 및 세션 생성
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "sqlite+aiosqlite:///./trading_game.db"

#create_async_engine을 사용하여 비동기 엔진을 생성
engine = create_async_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

#async_sessionmaker를 사용하여 세션 로컬 클래스를 생성
async_session = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

# ORM 모델용 베이스 클래스
class Base(DeclarativeBase):
    pass


async def get_db():
    """비동기 DB 세션 생성 및 반환"""
        #async_session을 사용하여 세션을 열고 yield로 반환
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()