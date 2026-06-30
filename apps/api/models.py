from sqlalchemy import Column, String, Text
from database import Base
import uuid

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    user_id = Column(String, nullable=True)


class WikiPage(Base):
    __tablename__ = "wiki_pages"

    slug = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


# ---------------- VERSIONING ----------------
class ArticleVersion(Base):
    __tablename__ = "article_versions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    article_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(String, nullable=True)


class WikiVersion(Base):
    __tablename__ = "wiki_versions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(String, nullable=True)


# ---------------- COMMENTS ----------------
class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    target_type = Column(String, nullable=False)  # "article" or "wiki"
    target_id = Column(String, nullable=False)
    user_id = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(String, nullable=True)