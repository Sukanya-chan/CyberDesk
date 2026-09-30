import { useEffect, useState } from "react";
import { fetchCourses } from "../../services/learning";
import type { Course } from "../../types/learning";

export function CourseCataloguePage({ onCourse }: { onCourse: (slug: string) => void }) {
  const [courses, setCourses] = useState<Course[]>([]);
  const [state, setState] = useState<"loading"|"success"|"error">("loading");
  const [error, setError] = useState("");
  useEffect(() => { fetchCourses().then((d)=>{setCourses(d);setState("success")}).catch((e:unknown)=>{setError(e instanceof Error?e.message:"Unable to load courses");setState("error")}); }, []);
  return <main>
    <div className="eyebrow">LEARNING SYSTEM</div><h1 className="page-title">Knowledge base.</h1>
    <p className="page-subtitle">Structured courses for cybersecurity fundamentals, administration, and practical security thinking.</p>
    {state==="loading" && <p className="loading" role="status">Loading courses…</p>}
    {state==="error" && <p className="alert" role="alert">{error}</p>}
    {state==="success" && courses.length===0 && <div className="card"><h2>No published courses yet.</h2><p>Published learning content will appear here.</p></div>}
    <section className="grid grid-3" style={{marginTop:24}}>
      {courses.map((course)=><article className="card" key={course.id}>
        <span className="tag">{course.category_name}</span><h2>{course.title}</h2><p>{course.description || "Explore this cybersecurity course."}</p>
        <div className="card-action"><span className="muted">Course</span><button className="primary" onClick={()=>onCourse(course.slug)}>Open course →</button></div>
      </article>)}
    </section>
  </main>;
}
