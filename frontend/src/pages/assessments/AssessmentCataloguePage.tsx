import { useEffect, useState } from "react";
import { fetchQuizzes } from "../../services/assessments";
import type { QuizSummary } from "../../types/assessment";

export function AssessmentCataloguePage({ onQuiz, onBack: _onBack }: { onQuiz:(id:number)=>void; onBack:()=>void }) {
  const [quizzes,setQuizzes]=useState<QuizSummary[]>([]); const [state,setState]=useState<"loading"|"success"|"error">("loading"); const [error,setError]=useState("");
  useEffect(()=>{fetchQuizzes().then(d=>{setQuizzes(d);setState("success")}).catch((e:unknown)=>{setError(e instanceof Error?e.message:"Unable to load assessments");setState("error")})},[]);
  return <main>
    <div className="eyebrow">ASSESSMENT LAB</div><h1 className="page-title">Prove what you know.</h1>
    <p className="page-subtitle">Short, scored assessments with immediate results. Select a quiz and work through every question.</p>
    {state==="loading"&&<p className="loading" role="status">Loading assessments…</p>}
    {state==="error"&&<p className="alert" role="alert">{error}</p>}
    {state==="success"&&quizzes.length===0&&<div className="card"><h2>No published assessments yet.</h2><p>Ask an administrator to publish a quiz.</p></div>}
    <section className="grid grid-2" style={{marginTop:24}}>
      {quizzes.map(q=><article className="card" key={q.id}><span className="tag">QUIZ / PUBLISHED</span><h2>{q.title}</h2><p>{q.description||"Cybersecurity knowledge assessment."}</p><div className="card-action"><span className="muted">Automatic scoring</span><button className="primary" onClick={()=>onQuiz(q.id)}>Start assessment →</button></div></article>)}
    </section>
  </main>;
}
