"use client";

import { useEffect, useState } from "react";

type Article = {
  id: string;
  title: string;
  content: string;
  author?: string;
  tags: string[];
};

export default function Home() {
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    fetch((process as any).env.API_URL + "/articles")
      .then((res) => res.json())
      .then((data) => setArticles(data));
  }, []);

  return (
    <main style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Pesquisa Aberta Brasil</h1>
      <p>Plataforma de ciência aberta</p>

      <h2>Artigos</h2>

      {articles.length === 0 && <p>Nenhum artigo ainda.</p>}

      {articles.map((a) => (
        <div key={a.id} style={{ border: "1px solid #ccc", margin: 10, padding: 10 }}>
          <h3>{a.title}</h3>
          <p>{a.content}</p>
          <small>{a.author}</small>
        </div>
      ))}
    </main>
  );
}