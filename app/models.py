# SQL Alchemy models declaration.
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
# mapped_column syntax from SQLAlchemy 2.0.

# https://alembic.sqlalchemy.org/en/latest/tutorial.html
# Note, it is used by alembic migrations logic, see `alembic/env.py`

# Alembic shortcuts:
# # create migration
# alembic revision --autogenerate -m "migration_name"

# # apply all migrations
# alembic upgrade head


import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Attorney(Base):
    __tablename__ = "attorneys"

    attorney_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] =mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(
        String(256), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    leads: Mapped[list["Lead"]] = relationship(back_populates="attorney")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="attorney")

class Prospect(Base):
    __tablename__ = "prospects"

    prospect_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(256), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    resume: Mapped[str] = mapped_column(String(128), nullable=False)
    leads: Mapped[list["Lead"]] = relationship(back_populates="prospect")


class Lead(Base):
    __tablename__ = "leads"
    lead_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    attorney_id: Mapped[str] = mapped_column(
        ForeignKey("attorneys.attorney_id", ondelete="CASCADE"),
    )
    prospect_id: Mapped[str] = mapped_column(
        ForeignKey("prospects.prospect_id", ondelete="CASCADE"),
    )
    state: Mapped[str] = mapped_column(
        String(64), nullable=False
    )
    attorney: Mapped["Attorney"] = relationship(back_populates="leads")
    prospect: Mapped["Prospect"] = relationship(back_populates="leads")

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    refresh_token: Mapped[str] = mapped_column(
        String(512), nullable=False, unique=True, index=True
    )
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    exp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    attorney_id: Mapped[str] = mapped_column(
        ForeignKey("attorneys.attorney_id", ondelete="CASCADE"),
    )
    attorney: Mapped["Attorney"] = relationship(back_populates="refresh_tokens")
