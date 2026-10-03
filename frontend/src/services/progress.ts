import { ApiError } from "./api";
import type { DashboardProgress, LessonProgress } from "../types/progress";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";
type GetToken = () => Promise<string | null>;

async function authed<T>(path: string, getToken: GetToken, init?: RequestInit): Promise<T> {
  const token = await getToken();
  if (!token) throw new ApiError("Not signed in", 401);
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      ...(init?.headers ?? {}),
      Authorization: `Bearer ${token}`,
      ...(init?.body ? {"Content-Type": "application/json"} : {}),
    },
  });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try { const data = await response.json(); message = data?.detail ?? data?.error?.message ?? message; } catch {}
    throw new ApiError(message, response.status);
  }
  return (await response.json()) as T;
}

export const fetchDashboardProgress = (getToken: GetToken) =>
  authed<DashboardProgress>("/progress/dashboard", getToken);

export const fetchLessonProgress = (lessonId: number, getToken: GetToken) =>
  authed<LessonProgress>(`/lessons/${lessonId}/progress`, getToken);

export const completeLesson = (lessonId: number, getToken: GetToken) =>
  authed<LessonProgress>(`/lessons/${lessonId}/complete`, getToken, { method: "POST" });
