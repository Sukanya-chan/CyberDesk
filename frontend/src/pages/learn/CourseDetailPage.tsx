import { useEffect,useState } from "react";
import { fetchCourse } from "../../services/learning";
import type { CourseDetail } from "../../types/learning";

export function CourseDetailPage({slug,onLesson,onBack}:{slug:string;onLesson:(lessonSlug:string)=>void;onBack:()=>void}) {
 const [course,setCourse]=useState<CourseDetail|null>(null);const [error,setError]=useState("");
 useEffect(()=>{setCourse(null);setError("");fetchCourse(slug).then(setCourse).catch((e:unknown)=>setError(e instanceof Error?e.message:"Unable to load course"))},[slug]);
 return <main>
  <button className="back" onClick={onBack}>← Learning</button>
  {error&&<p className="alert" role="alert">{error}</p>}
  {course&&<>
   <section className="hero"><span className="eyebrow">COURSE / {course.modules.length} MODULES</span><h1 className="page-title">{course.title}</h1><p className="page-subtitle">{course.description}</p></section>
   <div className="section-head"><h2>Course modules</h2><span className="muted">Select a lesson to continue</span></div>
   <section className="stack">{course.modules.map((m,i)=><article className="card" key={m.id}>
    <div style={{display:"flex",justifyContent:"space-between",gap:16}}><div><span className="eyebrow">MODULE {String(i+1).padStart(2,"0")}</span><h2>{m.title}</h2></div><span className="tag">{m.lessons.length} lessons</span></div>
    {m.lessons.length===0?<p>No published lessons in this module yet.</p>:<div className="stack">{m.lessons.map(l=><button key={l.id} onClick={()=>onLesson(l.slug)} style={{textAlign:"left"}}>◇ {l.title}<span className="muted" style={{float:"right"}}>Open →</span></button>)}</div>}
   </article>)}</section>
  </>}
 </main>;
}
