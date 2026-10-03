import { useAuth } from "@clerk/react";
import { useEffect,useState } from "react";
import { fetchLesson } from "../../services/learning";
import { completeLesson, fetchLessonProgress } from "../../services/progress";
import type { Lesson } from "../../types/learning";

export function LessonPage({courseSlug,lessonSlug,onBack}:{courseSlug:string;lessonSlug:string;onBack:()=>void}) {
 const { getToken } = useAuth();
 const [lesson,setLesson]=useState<Lesson|null>(null); const [completed,setCompleted]=useState(false);
 const [error,setError]=useState(""); const [saving,setSaving]=useState(false);
 useEffect(()=>{let cancelled=false;setLesson(null);setError("");
   fetchLesson(courseSlug,lessonSlug).then(async data=>{if(cancelled)return;setLesson(data);
     try { const p=await fetchLessonProgress(data.id,getToken); if(!cancelled)setCompleted(p.completed); } catch {}
   }).catch((e:unknown)=>{if(!cancelled)setError(e instanceof Error?e.message:"Unable to load lesson")});
   return ()=>{cancelled=true};
 },[courseSlug,lessonSlug,getToken]);
 async function markComplete(){if(!lesson)return;setSaving(true);setError("");try{await completeLesson(lesson.id,getToken);setCompleted(true)}catch(e){setError(e instanceof Error?e.message:"Unable to save progress")}finally{setSaving(false)}}
 return <main>
  <button className="back" onClick={onBack}>← Course</button>
  {error&&<p className="alert" role="alert">{error}</p>}
  {lesson&&<article className="card" style={{maxWidth:850,margin:"0 auto"}}>
    <span className="eyebrow">LESSON / ACTIVE</span><h1 className="page-title" style={{fontSize:"2.5rem"}}>{lesson.title}</h1>
    <div className="lesson-content">{lesson.content}</div>
    <div className="card-action">
      <span className={`tag ${completed ? "success" : ""}`}>{completed ? "COMPLETED" : "IN PROGRESS"}</span>
      {!completed && <button className="primary" onClick={markComplete} disabled={saving}>{saving ? "Saving…" : "Mark complete →"}</button>}
    </div>
  </article>}
 </main>;
}
