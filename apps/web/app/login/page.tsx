"use client";

import { useState } from "react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [msg, setMsg] = useState("");

  async function submit() {
    setMsg("");

    const res = await fetch((process as any).env.API_URL + `/auth/${mode}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    setMsg(JSON.stringify(data));
  }

  return (
    <main style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>{mode === "login" ? "Login" : "Cadastro"}</h1>

      <input placeholder="usuário" value={username} onChange={e => setUsername(e.target.value)} /><br /><br />
      <input placeholder="senha" type="password" value={password} onChange={e => setPassword(e.target.value)} /><br /><br />

      <button onClick={submit}>
        {mode === "login" ? "Entrar" : "Criar conta"}
      </button>

      <p>{msg}</p>

      <button onClick={() => setMode(mode === "login" ? "register" : "login")}>
        Trocar para {mode === "login" ? "Cadastro" : "Login"}
      </button>
    </main>
  );
}