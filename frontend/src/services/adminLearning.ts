import type { AdminLesson, AdminModule, Category, Course } from "../types/learning";
import { ApiError } from "./api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";
type GetToken = () => Promise<string | null>;

async function request<T>(path: string, getToken: GetToken, init: RequestInit = {}): Promise<T> {
  const token = await getToken();
  if (!token) throw new ApiError("Not signed in", 401);

  const headers = new Headers(init.headers);
  headers.set("Authorization", `Bearer ${token}`);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");

  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      message = body?.error?.message ?? body?.detail ?? message;
    } catch {}
    throw new ApiError(message, response.status);
  }
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export const admin = {
  categories: (token: GetToken) => request<Category[]>("/admin/categories", token),
  createCategory: (token: GetToken, body: object) =>
    request<Category>("/admin/categories", token, { method: "POST", body: JSON.stringify(body) }),
  updateCategory: (token: GetToken, id: number, body: object) =>
    request<Category>(`/admin/categories/${id}`, token, { method: "PATCH", body: JSON.stringify(body) }),
  deleteCategory: (token: GetToken, id: number) =>
    request<void>(`/admin/categories/${id}`, token, { method: "DELETE" }),

  courses: (token: GetToken) => request<Course[]>("/admin/courses", token),
  createCourse: (token: GetToken, body: object) =>
    request<Course>("/admin/courses", token, { method: "POST", body: JSON.stringify(body) }),
  updateCourse: (token: GetToken, id: number, body: object) =>
    request<Course>(`/admin/courses/${id}`, token, { method: "PATCH", body: JSON.stringify(body) }),
  deleteCourse: (token: GetToken, id: number) =>
    request<void>(`/admin/courses/${id}`, token, { method: "DELETE" }),

  modules: (token: GetToken, courseId: number) =>
    request<AdminModule[]>(`/admin/courses/${courseId}/modules`, token),
  createModule: (token: GetToken, body: object) =>
    request<AdminModule>("/admin/modules", token, { method: "POST", body: JSON.stringify(body) }),
  updateModule: (token: GetToken, id: number, body: object) =>
    request<AdminModule>(`/admin/modules/${id}`, token, { method: "PATCH", body: JSON.stringify(body) }),
  deleteModule: (token: GetToken, id: number) =>
    request<void>(`/admin/modules/${id}`, token, { method: "DELETE" }),
  reorderModules: (token: GetToken, courseId: number, orderedIds: number[]) =>
    request<AdminModule[]>(`/admin/courses/${courseId}/modules/reorder`, token, {
      method: "PATCH",
      body: JSON.stringify({ ordered_ids: orderedIds }),
    }),

  lessons: (token: GetToken, moduleId: number) =>
    request<AdminLesson[]>(`/admin/modules/${moduleId}/lessons`, token),
  createLesson: (token: GetToken, body: object) =>
    request<AdminLesson>("/admin/lessons", token, { method: "POST", body: JSON.stringify(body) }),
  updateLesson: (token: GetToken, id: number, body: object) =>
    request<AdminLesson>(`/admin/lessons/${id}`, token, { method: "PATCH", body: JSON.stringify(body) }),
  deleteLesson: (token: GetToken, id: number) =>
    request<void>(`/admin/lessons/${id}`, token, { method: "DELETE" }),
  reorderLessons: (token: GetToken, moduleId: number, orderedIds: number[]) =>
    request<AdminLesson[]>(`/admin/modules/${moduleId}/lessons/reorder`, token, {
      method: "PATCH",
      body: JSON.stringify({ ordered_ids: orderedIds }),
    }),
};
