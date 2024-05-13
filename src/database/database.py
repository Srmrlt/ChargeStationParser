from functools import wraps

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = create_async_engine(
    url=settings.db_url,
    echo=False,
)

session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def session_manager(func):
    """
    Decorates an async function to manage an SQLAlchemy session, handling
    creation, commit, and rollback. It injects a session as the first argument to the
    function, managing session lifecycle within the operation.

    Args:
        func (Callable): An async function that accepts an `AsyncSession`.

    Returns:
        Callable: A function wrapped with session management.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_factory() as session:
            try:
                # Передаём session как первый аргумент после self в метод класса
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e

    return wrapper


class Base(DeclarativeBase):
    """
    Define a base class for all SQLAlchemy Declarative models.
    It provides a common __repr__ method and a mapping from type annotations to SQLAlchemy types.
    """

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
