import { useEffect, useState } from "react";
import { fetchLesson } from "../../services/learning";
import type { Lesson } from "../../types/learning";

export function LessonPage({
  courseSlug,
  lessonSlug,
  onBack,
}: {
  courseSlug: string;
  lessonSlug: string;
  onBack: () => void;
}) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    setLesson(null);
    setError("");
    fetchLesson(courseSlug, lessonSlug)
      .then(setLesson)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : "Unable to load lesson"));
  }, [courseSlug, lessonSlug]);

  return (
    <main>
      <button type="button" onClick={onBack}>← Course</button>
      {error && <p role="alert">{error}</p>}
      {lesson && (
        <article>
          <h1>{lesson.title}</h1>
          <p style={{ whiteSpace: "pre-wrap" }}>{lesson.content}</p>
        </article>
      )}
    </main>
  );
}
