"use client";

import { useEffect, useState } from "react";

type Result = {
  articles: { id: string; title: string; type: string }[];
  wiki: { slug: string; title: string; type: string }[];
};

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [data, setData] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);

  async function search() {
    if (!q) return;
    setLoading(true);

    const res = await fetch((process as any).env.API_URL + "/search?q=" + encodeURIComponent(q));
    const json = await res.json();

    setData(json);
    setLoading(false);
  }

  useEffect(() => {
    const delay = setTimeout(() => {
      if (q) search();
    }, 400);

    return () => clearTimeout(delay);
  }, [q]);

  return (
    <main style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Busca Global</h1>

      <input
        placeholder="Pesquisar artigos e wiki..."
        value={q}
        onChange={(e) => setQ(e.target.value)}
        style={{ width: "100%", padding: 10 }}
      />

      {loading && <p>Buscando...</p>}

      {data && (
        <>
          <h2>Artigos</h2>
          {data.articles.length === 0 && <p>Nenhum artigo encontrado.</p>}

          {data.articles.map((a) => (
            <div key={a.id} style={{ border: "1px solid #ccc", margin: 10, padding: 10 }}>
              <a href={`/article/${a.id}`}>{a.title}</a>
            </div>
          ))}

          <h2>Wiki</h2>
          {data.wiki.length === 0 && <p>Nenhuma página encontrada.</p>}

          {data.wiki.map((w) => (
            <div key={w.slug} style={{ border: "1px solid #ccc", margin: 10, padding: 10 }}>
              <a href={`/wiki/${w.slug}`}>{w.title}</a>
            </div>
          ))}
        </>
      )}
    </main>
  );
}