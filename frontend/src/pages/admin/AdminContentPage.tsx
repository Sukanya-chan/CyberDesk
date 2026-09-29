import { useAuth } from "@clerk/react";
import { useEffect, useState } from "react";
import { admin } from "../../services/adminLearning";
import type { AdminLesson, AdminModule, Category, Course } from "../../types/learning";

export function AdminContentPage({ onBack }: { onBack: () => void }) {
  const { getToken } = useAuth();
  const [categories, setCategories] = useState<Category[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [modules, setModules] = useState<AdminModule[]>([]);
  const [lessons, setLessons] = useState<AdminLesson[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<number | null>(null);
  const [selectedModule, setSelectedModule] = useState<number | null>(null);
  const [message, setMessage] = useState("");

  const reload = async () => {
    const [cats, courseData] = await Promise.all([
      admin.categories(getToken),
      admin.courses(getToken),
    ]);
    setCategories(cats);
    setCourses(courseData);
  };

  useEffect(() => {
    reload().catch((e: unknown) =>
      setMessage(e instanceof Error ? e.message : "Admin load failed")
    );
  }, []);

  const addCategory = async () => {
    const name = window.prompt("Category name");
    if (!name) return;
    await admin.createCategory(getToken, { name });
    await reload();
  };

  const addCourse = async () => {
    const category = categories[0];
    if (!category) {
      setMessage("Create a category first.");
      return;
    }
    const title = window.prompt("Course title");
    if (!title) return;
    const slug =
      window.prompt("Course slug", title.toLowerCase().replace(/[^a-z0-9]+/g, "-")) || "";
    await admin.createCourse(getToken, {
      category_id: category.id,
      title,
      slug,
      status: "draft",
    });
    await reload();
  };

  const loadModules = async (courseId: number) => {
    setSelectedCourse(courseId);
    setSelectedModule(null);
    setLessons([]);
    setModules(await admin.modules(getToken, courseId));
  };

  const addModule = async () => {
    if (!selectedCourse) return;
    const title = window.prompt("Module title");
    if (!title) return;
    await admin.createModule(getToken, { course_id: selectedCourse, title });
    await loadModules(selectedCourse);
  };

  const loadLessons = async (moduleId: number) => {
    setSelectedModule(moduleId);
    setLessons(await admin.lessons(getToken, moduleId));
  };

  const addLesson = async () => {
    if (!selectedModule) return;
    const title = window.prompt("Lesson title");
    if (!title) return;
    const slug =
      window.prompt("Lesson slug", title.toLowerCase().replace(/[^a-z0-9]+/g, "-")) || "";
    const content = window.prompt("Lesson content", "Add educational content here.") || "";
    await admin.createLesson(getToken, {
      module_id: selectedModule,
      title,
      slug,
      content,
      status: "draft",
    });
    await loadLessons(selectedModule);
  };

  const toggleCourse = async (course: Course) => {
    await admin.updateCourse(getToken, course.id, { status: "published" });
    await reload();
  };

  const toggleLesson = async (lesson: AdminLesson) => {
    await admin.updateLesson(getToken, lesson.id, {
      status: lesson.status === "published" ? "draft" : "published",
    });
    if (selectedModule) await loadLessons(selectedModule);
  };

  return (
    <main>
      <button type="button" onClick={onBack}>← Account</button>
      <h1>Admin Content</h1>
      {message && <p role="alert">{message}</p>}

      <section>
        <h2>Categories</h2>
        <button type="button" onClick={() => addCategory().catch((e: unknown) =>
          setMessage(e instanceof Error ? e.message : "Could not create category")
        )}>Add category</button>
        <ul>{categories.map((c) => <li key={c.id}>{c.name}</li>)}</ul>
      </section>

      <section>
        <h2>Courses</h2>
        <button type="button" onClick={() => addCourse().catch((e: unknown) =>
          setMessage(e instanceof Error ? e.message : "Could not create course")
        )}>Add course</button>
        <ul>
          {courses.map((course) => (
            <li key={course.id}>
              <button type="button" onClick={() => loadModules(course.id)}>
                {course.title}
              </button>{" "}
              — {course.slug}
              <button type="button" onClick={() => toggleCourse(course)}>
                Publish
              </button>
            </li>
          ))}
        </ul>
      </section>

      {selectedCourse !== null && (
        <section>
          <h2>Modules</h2>
          <button type="button" onClick={() => addModule().catch((e: unknown) =>
            setMessage(e instanceof Error ? e.message : "Could not create module")
          )}>Add module</button>
          <ul>
            {modules.map((module) => (
              <li key={module.id}>
                <button type="button" onClick={() => loadLessons(module.id)}>
                  {module.title}
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {selectedModule !== null && (
        <section>
          <h2>Lessons</h2>
          <button type="button" onClick={() => addLesson().catch((e: unknown) =>
            setMessage(e instanceof Error ? e.message : "Could not create lesson")
          )}>Add lesson</button>
          <ul>
            {lessons.map((lesson) => (
              <li key={lesson.id}>
                {lesson.title} ({lesson.status}){" "}
                <button type="button" onClick={() => toggleLesson(lesson)}>
                  {lesson.status === "published" ? "Unpublish" : "Publish"}
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
