import {useEffect,useState} from "react";
import {useAuth} from "@clerk/react";
import {fetchChallenge,fetchChallengeProgress,submitChallenge} from "../../services/challenges";
import type {Challenge,ChallengeProgress,ChallengeSubmissionResponse} from "../../types/challenge";

export function ChallengePage({challengeId,onBack}:{challengeId:number;onBack:()=>void}) {
 const {getToken}=useAuth();const [challenge,setChallenge]=useState<Challenge|null>(null);const [progress,setProgress]=useState<ChallengeProgress|null>(null);const [flag,setFlag]=useState("");const [result,setResult]=useState<ChallengeSubmissionResponse|null>(null);const [state,setState]=useState<"loading"|"ready"|"submitting"|"error">("loading");const [error,setError]=useState("");
 useEffect(()=>{Promise.all([fetchChallenge(challengeId),fetchChallengeProgress(challengeId,getToken)]).then(([d,p])=>{setChallenge(d);setProgress(p);setState("ready")}).catch((e:unknown)=>{setError(e instanceof Error?e.message:"Unable to load challenge");setState("error")})},[challengeId,getToken]);
 async function handleSubmit(){if(!flag.trim())return;setState("submitting");try{const r=await submitChallenge(challengeId,flag,getToken);setResult(r);if(r.correct)setProgress({solved:true,points_earned:r.points_awarded});setFlag("");setState("ready")}catch(e:unknown){setError(e instanceof Error?e.message:"Unable to submit flag");setState("error")}}
 if(state==="loading")return <main><p className="loading" role="status">Loading challenge…</p></main>;
 if(state==="error"&&!challenge)return <main><button className="back" onClick={onBack}>← Challenges</button><p className="alert" role="alert">{error}</p></main>;
 if(!challenge)return null;
 return <main>
  <button className="back" onClick={onBack}>← Challenge lab</button>
  <section className="hero"><span className="eyebrow">CYBER LAB / {challenge.category}</span><h1 className="page-title">{challenge.title}</h1><div style={{display:"flex",gap:8,flexWrap:"wrap"}}><span className="tag">{challenge.difficulty}</span><span className="tag">★ {challenge.points} XP</span><span className="tag">FLAG VALIDATION</span></div></section>
  <div className="grid grid-2" style={{marginTop:18}}>
   <div className="card"><h2>Mission</h2><p>{challenge.description}</p>{challenge.instructions&&<><h3>Instructions</h3><p>{challenge.instructions}</p></>}</div>
   <div className="card"><h2>Submit flag</h2><p className="muted">Only submit the flag discovered through the challenge. Nothing is executed.</p>{progress?.solved?<p className="success" role="status">Solved — {progress.points_earned} XP earned.</p>:<><input value={flag} onChange={e=>setFlag(e.target.value)} placeholder="CYBERDESK{...}" disabled={state==="submitting"}/><button className="primary" style={{marginTop:12}} disabled={state==="submitting"||!flag.trim()} onClick={handleSubmit}>{state==="submitting"?"Validating…":"Submit flag →"}</button></>}{result&&!result.correct&&<p className="alert" role="alert">{result.message} Try again.</p>}{state==="error"&&<p className="alert" role="alert">{error}</p>}</div>
  </div>
  {challenge.hint&&<details className="card" style={{marginTop:16}}><summary>Need a hint?</summary><p>{challenge.hint}</p></details>}
 </main>;
}
