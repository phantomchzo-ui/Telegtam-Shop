from typing import Optional


from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=True
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass



class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(25), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean,default=False, nullable=False)


class Photo(Base):
    __tablename__ = 'photos'

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(256))
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))




