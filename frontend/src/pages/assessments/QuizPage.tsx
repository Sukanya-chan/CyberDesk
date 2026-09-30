import {useEffect,useState} from "react";
import {useAuth} from "@clerk/react";
import {fetchQuiz,submitQuiz} from "../../services/assessments";
import type {QuizAttemptResponse,QuizDetail} from "../../types/assessment";

export function QuizPage({quizId,onBack}:{quizId:number;onBack:()=>void}) {
 const {getToken}=useAuth();const [quiz,setQuiz]=useState<QuizDetail|null>(null);const [answers,setAnswers]=useState<Record<number,number>>({});const [result,setResult]=useState<QuizAttemptResponse|null>(null);const [state,setState]=useState<"loading"|"ready"|"submitting"|"error">("loading");const [error,setError]=useState("");
 useEffect(()=>{fetchQuiz(quizId).then(d=>{setQuiz(d);setState("ready")}).catch((e:unknown)=>{setError(e instanceof Error?e.message:"Unable to load quiz");setState("error")})},[quizId]);
 async function handleSubmit(){if(!quiz)return;setState("submitting");try{const r=await submitQuiz(quiz.id,quiz.questions.map(q=>({question_id:q.id,option_id:answers[q.id]??null})),getToken);setResult(r);setState("ready")}catch(e:unknown){setError(e instanceof Error?e.message:"Unable to submit quiz");setState("error")}}
 if(state==="loading")return <main><p className="loading" role="status">Loading assessment…</p></main>;
 if(state==="error"&&!quiz)return <main><button className="back" onClick={onBack}>← Assessments</button><p className="alert" role="alert">{error}</p></main>;
 if(!quiz)return null;
 const answered=Object.keys(answers).length;
 return <main>
  <button className="back" onClick={onBack}>← Assessments</button>
  <div className="eyebrow">ASSESSMENT / {answered} OF {quiz.questions.length} ANSWERED</div><h1 className="page-title" style={{fontSize:"2.6rem"}}>{quiz.title}</h1><p className="page-subtitle">{quiz.description}</p>
  {result?<section className="result"><div className="eyebrow">ASSESSMENT COMPLETE</div><div className="score">{Math.round((result.score/Math.max(result.total_questions,1))*100)}%</div><h2>{result.score} / {result.total_questions} correct</h2><p className="muted">Your result has been recorded.</p><button className="primary" onClick={()=>{setResult(null);setAnswers({})}}>Try again</button></section>:
  <><section>{quiz.questions.map((q,index)=><fieldset key={q.id}><legend>{String(index+1).padStart(2,"0")} · {q.question_text}</legend>{q.options.slice().sort((a,b)=>a.position-b.position).map(o=><label className="option" key={o.id}><input type="radio" name={`question-${q.id}`} checked={answers[q.id]===o.id} onChange={()=>setAnswers(cur=>({...cur,[q.id]:o.id}))}/>{o.option_text}</label>)}</fieldset>)}</section>
  {state==="error"&&<p className="alert" role="alert">{error}</p>}<button className="primary" disabled={state==="submitting"||quiz.questions.length===0} onClick={handleSubmit}>{state==="submitting"?"Checking result…":"Submit assessment →"}</button></>}
 </main>;
}
