from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum
from config import settings

Base = declarative_base()

# ----------------------------------------
# ENUM: 読書状態
# ----------------------------------------
class ReadingStatus(enum.Enum):
    wishlist = "wishlist"
    reading = "reading"
    finished = "finished"

# ----------------------------------------
# Users
# ----------------------------------------
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )

# ----------------------------------------
# Books（本のマスタ）
# ----------------------------------------
class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    isbn = Column(String)
    cover_url = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )

# ----------------------------------------
# UserBooks（ユーザー固有の状態・メモなど）
# ----------------------------------------
class UserBook(Base):
    __tablename__ = "user_books"
    __table_args__ = {"schema": settings.SCHEMA_NAME}

    id = Column(Integer, primary_key=True)

    user_id = Column(
        ForeignKey(f"{settings.SCHEMA_NAME}.users.id", ondelete="CASCADE"),
        nullable=False
    )
    book_id = Column(
        ForeignKey(f"{settings.SCHEMA_NAME}.books.id", ondelete="CASCADE"),
        nullable=False
    )

    status = Column(
        Enum(ReadingStatus, name="reading_status"),
        nullable=False,
        default=ReadingStatus.wishlist
    )

    # --- おすすめ情報 ---
    recommended_by = Column(String)
    source = Column(String)
    recommended_at = Column(Date)

    # --- 読了情報 ---
    rating = Column(Integer)
    review = Column(Text)
    finished_at = Column(Date)

    # --- 汎用メモ ---
    note = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

