from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models

# Cria tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pesquisa Aberta Brasil API")

# ---------- Schemas ----------
class ArticleCreate(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    tags: List[str] = []

class ArticleOut(ArticleCreate):
    id: str

# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "Pesquisa Aberta Brasil API ativa"}

@app.post("/articles", response_model=ArticleOut)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = models.Article(
        title=article.title,
        content=article.content,
        author=article.author,
        tags=",".join(article.tags) if article.tags else None
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return ArticleOut(
        id=db_article.id,
        title=db_article.title,
        content=db_article.content,
        author=db_article.author,
        tags=db_article.tags.split(",") if db_article.tags else []
    )

@app.get("/articles", response_model=List[ArticleOut])
def list_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return [
        ArticleOut(
            id=a.id,
            title=a.title,
            content=a.content,
            author=a.author,
            tags=a.tags.split(",") if a.tags else []
        )
        for a in articles
    ]

@app.get("/articles/{article_id}")
def get_article(article_id: str, db: Session = Depends(get_db)):
    a = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not a:
        return {"error": "not found"}

    return ArticleOut(
        id=a.id,
        title=a.title,
        content=a.content,
        author=a.author,
        tags=a.tags.split(",") if a.tags else []
    )