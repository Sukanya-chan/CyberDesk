import type {
  Challenge,
  ChallengeProgress,
  ChallengeSubmissionResponse,
} from "../types/challenge";
import { ApiError } from "./api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";
type GetToken = () => Promise<string | null>;

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) throw new ApiError(`Request failed (${response.status})`, response.status);
  return (await response.json()) as T;
}

async function authedJson<T>(path: string, getToken: GetToken): Promise<T> {
  const token = await getToken();
  if (!token) throw new ApiError("Not signed in", 401);
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new ApiError(`Request failed (${response.status})`, response.status);
  return (await response.json()) as T;
}

async function postJson<T>(path: string, body: unknown, getToken: GetToken): Promise<T> {
  const token = await getToken();
  if (!token) throw new ApiError("Not signed in", 401);
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
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

export const fetchChallenges = () => getJson<Challenge[]>("/challenges");
export const fetchChallenge = (challengeId: number) => getJson<Challenge>(`/challenges/${challengeId}`);
export const fetchChallengeProgress = (challengeId: number, getToken: GetToken) =>
  authedJson<ChallengeProgress>(`/challenges/${challengeId}/progress`, getToken);
export const submitChallenge = (challengeId: number, flag: string, getToken: GetToken) =>
  postJson<ChallengeSubmissionResponse>(`/challenges/${challengeId}/submit`, { flag }, getToken);
