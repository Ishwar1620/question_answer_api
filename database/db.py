from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from settings import config
from typing import AsyncGenerator
import uuid

# Global database instance
_db = None

class Database:
    def __init__(self):
        self.database_url = config.DATABASE_URL
        echo = False
        self.engine = create_async_engine(
            self.database_url,
            echo=echo,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            connect_args={
                "statement_cache_size": 0,                        
                "prepared_statement_name_func": lambda: f"ps_{uuid.uuid4().hex}",
            },
        )
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self.base = declarative_base()
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


def get_db():
    """Get global database instance."""
    global _db
    if _db is None:
        _db = Database()
    return _db


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db = get_db()
    async with db.AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 