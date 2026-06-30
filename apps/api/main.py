from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid

app = FastAPI(title="Pesquisa Aberta Brasil API")

class Article(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    author: Optional[str] = None
    tags: List[str] = []

# Simples banco em memória (MVP)
DB: Dict[str, Article] = {}

@app.get("/")
def root():
    return {"message": "Pesquisa Aberta Brasil API ativa"}

@app.post("/articles")
def create_article(article: Article):
    article_id = str(uuid.uuid4())
    article.id = article_id
    DB[article_id] = article
    return article

@app.get("/articles")
def list_articles():
    return list(DB.values())

@app.get("/articles/{article_id}")
def get_article(article_id: str):
    return DB.get(article_id, {"error": "not found"})