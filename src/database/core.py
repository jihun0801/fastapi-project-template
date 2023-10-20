from typing import Any

from sqlalchemy import CursorResult, Delete, Insert, Select, Update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

DATABASE_URL = str(settings.DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


AsyncSessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db_session() -> AsyncSession:
    db_session = AsyncSessionLocal()
    try:
        yield db_session
    finally:
        await db_session.close()


async def fetch_one(
    db_session: AsyncSession, query: Select | Insert | Update
) -> dict[str, Any] | None:
    cursor: CursorResult = await db_session.execute(query)
    return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(
    db_session: AsyncSession, query: Select | Insert | Update
) -> list[dict[str, Any]]:
    cursor: CursorResult = await db_session.execute(query)
    return [r._asdict() for r in cursor.all()]


async def execute(db_session: AsyncSession, query: Insert | Update | Delete) -> None:
    await db_session.execute(query)
