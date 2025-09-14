#app/model.py
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    words: Mapped[List['UserWord']] = relationship(back_populates="user")

class Word(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    english : Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    russian: Mapped[str] = mapped_column( nullable=False)

    users: Mapped[List['UserWord']] = relationship(back_populates="word")

class UserWord(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    progress : Mapped[int] = mapped_column(default=0)

    user : Mapped['User'] = relationship(back_populates="words")
    word : Mapped["Word"] = relationship(back_populates="users")
