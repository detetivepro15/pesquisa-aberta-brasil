from sqlalchemy import Column, String, Text
from database import Base
import uuid

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, nullable=True)
    tags = Column(String, nullable=True)  # armazenado como string separada por vírgulas


class WikiPage(Base):
    __tablename__ = "wiki_pages"

    slug = Column(String, primary_key=True)  # URL amigável
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
