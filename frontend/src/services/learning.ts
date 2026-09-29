import type { Category, Course, CourseDetail, Lesson } from "../types/learning";
import { ApiError } from "./api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      message = body?.error?.message ?? body?.detail ?? message;
    } catch {}
    throw new ApiError(message, response.status);
  }
  return (await response.json()) as T;
}

export const fetchCategories = () => getJson<Category[]>("/categories");
export const fetchCourses = () => getJson<Course[]>("/courses");
export const fetchCourse = (slug: string) =>
  getJson<CourseDetail>(`/courses/${encodeURIComponent(slug)}`);
export const fetchLesson = (courseSlug: string, lessonSlug: string) =>
  getJson<Lesson>(
    `/lessons/${encodeURIComponent(courseSlug)}/${encodeURIComponent(lessonSlug)}`
  );
