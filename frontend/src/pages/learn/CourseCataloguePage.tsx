import { useEffect, useState } from "react";
import { fetchCourses } from "../../services/learning";
import type { Course } from "../../types/learning";

export function CourseCataloguePage({ onCourse }: { onCourse: (slug: string) => void }) {
  const [courses, setCourses] = useState<Course[]>([]);
  const [state, setState] = useState<"loading" | "success" | "error">("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCourses()
      .then((data) => {
        setCourses(data);
        setState("success");
      })
      .catch((e: unknown) => {
        setError(e instanceof Error ? e.message : "Unable to load courses");
        setState("error");
      });
  }, []);

  return (
    <main>
      <h1>CyberDesk Learning</h1>
      {state === "loading" && <p role="status">Loading courses…</p>}
      {state === "error" && <p role="alert">{error}</p>}
      {state === "success" && courses.length === 0 && <p>No published courses yet.</p>}
      {courses.map((course) => (
        <article key={course.id}>
          <h2>{course.title}</h2>
          <p>{course.description}</p>
          <small>{course.category_name}</small>
          <br />
          <button type="button" onClick={() => onCourse(course.slug)}>Open course</button>
        </article>
      ))}
    </main>
  );
}
