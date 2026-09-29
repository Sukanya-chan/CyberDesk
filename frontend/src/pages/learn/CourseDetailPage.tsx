import { useEffect, useState } from "react";
import { fetchCourse } from "../../services/learning";
import type { CourseDetail } from "../../types/learning";

export function CourseDetailPage({
  slug,
  onLesson,
  onBack,
}: {
  slug: string;
  onLesson: (lessonSlug: string) => void;
  onBack: () => void;
}) {
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    setCourse(null);
    setError("");
    fetchCourse(slug)
      .then(setCourse)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : "Unable to load course"));
  }, [slug]);

  return (
    <main>
      <button type="button" onClick={onBack}>← Courses</button>
      {error && <p role="alert">{error}</p>}
      {course && (
        <>
          <h1>{course.title}</h1>
          <p>{course.description}</p>
          {course.modules.map((module) => (
            <section key={module.id}>
              <h2>{module.title}</h2>
              {module.lessons.length === 0 ? (
                <p>No published lessons in this module yet.</p>
              ) : (
                <ul>
                  {module.lessons.map((lesson) => (
                    <li key={lesson.id}>
                      <button type="button" onClick={() => onLesson(lesson.slug)}>
                        {lesson.title}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          ))}
        </>
      )}
    </main>
  );
}
