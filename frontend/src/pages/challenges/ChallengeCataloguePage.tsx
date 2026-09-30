import { useEffect,useState } from "react";
import { fetchChallenges } from "../../services/challenges";
import type { Challenge } from "../../types/challenge";

export function ChallengeCataloguePage({onChallenge,onBack:_onBack}:{onChallenge:(id:number)=>void;onBack:()=>void}) {
 const [challenges,setChallenges]=useState<Challenge[]>([]);const [state,setState]=useState<"loading"|"success"|"error">("loading");const [error,setError]=useState("");
 useEffect(()=>{fetchChallenges().then(d=>{setChallenges(d);setState("success")}).catch((e:unknown)=>{setError(e instanceof Error?e.message:"Unable to load challenges");setState("error")})},[]);
 return <main>
  <div className="eyebrow">SAFE CYBER LAB</div><h1 className="page-title">Break things. Safely.</h1>
  <p className="page-subtitle">Flag-based challenges designed for controlled practice. No arbitrary code execution, scanning, or destructive actions.</p>
  {state==="loading"&&<p className="loading" role="status">Loading challenges…</p>}
  {state==="error"&&<p className="alert" role="alert">{error}</p>}
  {state==="success"&&challenges.length===0&&<div className="card"><h2>No published challenges yet.</h2><p>Published labs will appear here.</p></div>}
  <section className="grid grid-3" style={{marginTop:24}}>
   {challenges.map(c=><article className="card" key={c.id}><span className="tag">{c.category} / {c.difficulty}</span><h2>{c.title}</h2><p>{c.description}</p><div className="card-action"><span className="muted">★ {c.points} XP</span><button className="primary" onClick={()=>onChallenge(c.id)}>Enter lab →</button></div></article>)}
  </section>
 </main>;
}
