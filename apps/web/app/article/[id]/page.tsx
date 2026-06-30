"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type Article = {
  id: string;
  title: string;
  content: string;
  author?: string;
  tags: string[];
};

export default function ArticlePage() {
  const params = useParams();
  const id = params?.id as string;

  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    fetch((process as any).env.API_URL + "/articles/" + id)
      .then((res) => res.json())
      .then((data) => {
        setArticle(data);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <main style={{ padding: 20 }}>Carregando...</main>;
  }

  if (!article || (article as any).error) {
    return <main style={{ padding: 20 }}>Artigo não encontrado</main>;
  }

  return (
    <main style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>{article.title}</h1>
      <p><b>Autor:</b> {article.author}</p>
      <p>{article.content}</p>
      <div>
        <b>Tags:</b> {article.tags.join(", ")}
      </div>
    </main>
  );
}