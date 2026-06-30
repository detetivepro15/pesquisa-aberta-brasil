"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type WikiPage = {
  slug: string;
  title: string;
  content: string;
};

export default function WikiHome() {
  const [pages, setPages] = useState<WikiPage[]>([]);

  useEffect(() => {
    fetch((process as any).env.API_URL + "/wiki")
      .then((res) => res.json())
      .then((data) => setPages(data));
  }, []);

  return (
    <main style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Wiki (Pesquisa Aberta Brasil)</h1>

      <Link href="/wiki/new">Criar nova página</Link>

      <h2>Páginas</h2>

      {pages.length === 0 && <p>Nenhuma página wiki ainda.</p>}

      {pages.map((p) => (
        <div key={p.slug} style={{ margin: 10, padding: 10, border: "1px solid #ccc" }}>
          <Link href={`/wiki/${p.slug}`}>{p.title}</Link>
        </div>
      ))}
    </main>
  );
}