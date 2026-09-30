import type {
  AttemptSummary,
  QuizAttemptResponse,
  QuizDetail,
  QuizSummary,
} from "../types/assessment";
import { ApiError } from "./api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

type GetToken = () => Promise<string | null>;

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) throw new ApiError(`Request failed (${response.status})`, response.status);
  return (await response.json()) as T;
}

async function postJson<T>(path: string, body: unknown, getToken: GetToken): Promise<T> {
  const token = await getToken();
  if (!token) throw new ApiError("Not signed in", 401);

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const data = await response.json();
      message = data?.detail ?? data?.error?.message ?? message;
    } catch {}
    throw new ApiError(message, response.status);
  }
  return (await response.json()) as T;
}

export const fetchQuizzes = () => getJson<QuizSummary[]>("/quizzes");
export const fetchQuiz = (quizId: number) => getJson<QuizDetail>(`/quizzes/${quizId}`);
export const submitQuiz = (
  quizId: number,
  answers: Array<{ question_id: number; option_id: number | null }>,
  getToken: GetToken,
) => postJson<QuizAttemptResponse>(`/quizzes/${quizId}/attempts`, { answers }, getToken);
export const fetchAttempts = (quizId: number, getToken: GetToken) =>
  (async () => {
    const token = await getToken();
    if (!token) throw new ApiError("Not signed in", 401);
    const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}/attempts`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new ApiError(`Request failed (${response.status})`, response.status);
    return (await response.json()) as AttemptSummary[];
  })();
