import { useEffect,useState } from "react";
import { fetchLesson } from "../../services/learning";
import type { Lesson } from "../../types/learning";

export function LessonPage({courseSlug,lessonSlug,onBack}:{courseSlug:string;lessonSlug:string;onBack:()=>void}) {
 const [lesson,setLesson]=useState<Lesson|null>(null);const [error,setError]=useState("");
 useEffect(()=>{setLesson(null);setError("");fetchLesson(courseSlug,lessonSlug).then(setLesson).catch((e:unknown)=>setError(e instanceof Error?e.message:"Unable to load lesson"))},[courseSlug,lessonSlug]);
 return <main>
  <button className="back" onClick={onBack}>← Course</button>
  {error&&<p className="alert" role="alert">{error}</p>}
  {lesson&&<article className="card" style={{maxWidth:850,margin:"0 auto"}}><span className="eyebrow">LESSON / ACTIVE</span><h1 className="page-title" style={{fontSize:"2.5rem"}}>{lesson.title}</h1><div className="lesson-content">{lesson.content}</div></article>}
 </main>;
}
