"use client";

import { useState } from "react";

export default function NewArticle() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [author, setAuthor] = useState("");
  const [tags, setTags] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function submit() {
    setLoading(true);
    setMessage("");

    const res = await fetch((process as any).env.API_URL + "/articles", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title,
        content,
        author,
        tags: tags.split(",").map(t => t.trim()).filter(Boolean)
      })
    });

    if (res.ok) {
      setMessage("Artigo publicado com sucesso!");
      setTitle("");
      setContent("");
      setAuthor("");
      setTags("");
    } else {
      setMessage("Erro ao publicar artigo");
    }

    setLoading(false);
  }

  return (
    <main style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Novo Artigo</h1>

      <input placeholder="Título" value={title} onChange={e => setTitle(e.target.value)} /><br /><br />
      <input placeholder="Autor" value={author} onChange={e => setAuthor(e.target.value)} /><br /><br />
      <input placeholder="Tags (separadas por vírgula)" value={tags} onChange={e => setTags(e.target.value)} /><br /><br />
      <textarea placeholder="Conteúdo" value={content} onChange={e => setContent(e.target.value)} rows={10} cols={50} /><br /><br />

      <button onClick={submit} disabled={loading}>
        {loading ? "Publicando..." : "Publicar"}
      </button>

      <p>{message}</p>
    </main>
  );
}