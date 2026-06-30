from fastapi import FastAPI, Depends, Query
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

class WikiCreate(BaseModel):
    slug: str
    title: str
    content: str

class WikiOut(WikiCreate):
    pass

# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "Pesquisa Aberta Brasil API ativa"}

# -------- Articles --------

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

# -------- Wiki (Wikipedia-like system) --------

@app.post("/wiki", response_model=WikiOut)
def create_wiki(page: WikiCreate, db: Session = Depends(get_db)):
    db_page = models.WikiPage(
        slug=page.slug,
        title=page.title,
        content=page.content
    )
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return page

@app.get("/wiki")
def list_wiki(db: Session = Depends(get_db)):
    pages = db.query(models.WikiPage).all()
    return pages

@app.get("/wiki/{slug}")
def get_wiki(slug: str, db: Session = Depends(get_db)):
    page = db.query(models.WikiPage).filter(models.WikiPage.slug == slug).first()
    if not page:
        return {"error": "not found"}
    return page

@app.put("/wiki/{slug}")
def update_wiki(slug: str, page: WikiCreate, db: Session = Depends(get_db)):
    db_page = db.query(models.WikiPage).filter(models.WikiPage.slug == slug).first()
    if not db_page:
        return {"error": "not found"}

    db_page.title = page.title
    db_page.content = page.content

    db.commit()
    db.refresh(db_page)

    return db_page

# -------- SEARCH --------
@app.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    query = f"%{q}%"

    articles = db.query(models.Article).filter(
        models.Article.title.ilike(query) |
        models.Article.content.ilike(query)
    ).all()

    wiki_pages = db.query(models.WikiPage).filter(
        models.WikiPage.title.ilike(query) |
        models.WikiPage.content.ilike(query)
    ).all()

    return {
        "articles": [
            {"id": a.id, "title": a.title, "type": "article"}
            for a in articles
        ],
        "wiki": [
            {"slug": w.slug, "title": w.title, "type": "wiki"}
            for w in wiki_pages
        ]
    }