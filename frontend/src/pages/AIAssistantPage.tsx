import { useAuth } from "@clerk/react";
import { useState } from "react";
import { askCyberDeskAI } from "../services/ai";

export function AIAssistantPage() {
  const { getToken } = useAuth();
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");
  const [model, setModel] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function ask() {
    if (!prompt.trim()) return;
    setLoading(true); setError(""); setAnswer("");
    try {
      const result = await askCyberDeskAI(prompt.trim(), "Cybersecurity learning assistant", getToken);
      setAnswer(result.answer); setModel(result.model);
    } catch (e) {
      setError(e instanceof Error ? e.message : "AI request failed");
    } finally { setLoading(false); }
  }

  return <main>
    <section className="hero">
      <div className="eyebrow">CYBERDESK / OPTIONAL AI</div>
      <h1 className="page-title">Ask the security tutor.</h1>
      <p className="page-subtitle">Gemini can explain concepts and guide learning. Core CyberDesk features do not depend on AI.</p>
    </section>
    <section className="card ai-panel">
      <label className="field-label" htmlFor="ai-prompt">Question</label>
      <textarea id="ai-prompt" value={prompt} onChange={e => setPrompt(e.target.value)}
        placeholder="Explain the CIA triad with a practical example…" rows={5} />
      <div className="card-action">
        <span className="muted">Defensive learning only</span>
        <button className="primary" onClick={ask} disabled={loading || !prompt.trim()}>{loading ? "Thinking…" : "Ask AI →"}</button>
      </div>
      {error && <p className="alert" role="alert">{error}</p>}
      {answer && <article className="ai-answer"><div className="eyebrow">AI RESPONSE {model && `// ${model}`}</div><p>{answer}</p></article>}
    </section>
  </main>;
}
