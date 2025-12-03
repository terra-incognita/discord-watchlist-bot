from typing import List
from typing import Optional
from typing_extensions import Annotated
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime

engine = create_engine("sqlite+pysqlite:///watchlist.db", echo=True)

class Base(DeclarativeBase):
    pass

votes = Table(
    "votes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("media_id", Integer, ForeignKey("media.id"), primary_key=True)
)

genre_to_media = Table(
    "genre_to_media",
    Base.metadata,
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
    Column("media_id", Integer, ForeignKey("media.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String(32))
    voted_media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary=votes,
        back_populates="voters"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, display_name={self.display_name!r}, username={self.username!r})"

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())
]

class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_title: Mapped[str] = mapped_column(String(128))
    title: Mapped[str] = mapped_column(String(128))
    release_date: Mapped[str] = mapped_column(String(64))
    poster_path: Mapped[str] = mapped_column(Text)
    overview: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(32))
    added: Mapped[timestamp]
    watched: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    genres: Mapped[List["Genre"]] = relationship(
        "Genre",
        secondary=genre_to_media,
        back_populates="media_list"
    )
    voters: Mapped[List["User"]] = relationship(
        "User",
        secondary=votes,
        back_populates="voted_media"
    )
    def __repr__(self) -> str:
        return f"Media(id={self.id!r}, type={self.type!r}, title={self.title!r})"

class Genre(Base):
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    media_list: Mapped[List["Media"]] = relationship(
        "Media",
        secondary=genre_to_media,
        back_populates="genres"
    )

Base.metadata.create_all(engine)
