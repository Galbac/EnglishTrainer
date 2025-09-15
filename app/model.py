# app/model.py
from datetime import datetime, UTC
from typing import List

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    words: Mapped[List['UserWord']] = relationship(back_populates="user")


class Word(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    english: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    russian: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[List['UserWord']] = relationship(back_populates="word")


class UserWord(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    progress: Mapped[int] = mapped_column(default=0)
    easiness: Mapped[float] = mapped_column(default=2.5, server_default="2.5")
    interval: Mapped[int] = mapped_column(default=0, server_default="0")
    next_review: Mapped[datetime] = mapped_column(default=datetime.now(UTC), server_default=sa.func.now())
    reviews_count: Mapped[int] = mapped_column(default=0, server_default="0")

    user: Mapped['User'] = relationship(back_populates="words")
    word: Mapped["Word"] = relationship(back_populates="users")
