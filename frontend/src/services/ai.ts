import { ApiError } from "./api";
import type { AIAssistResponse } from "../types/ai";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";
type GetToken = () => Promise<string | null>;

export async function askCyberDeskAI(prompt: string, context: string, getToken: GetToken): Promise<AIAssistResponse> {
  const token = await getToken();
  if (!token) throw new ApiError("Not signed in", 401);
  const response = await fetch(`${API_BASE_URL}/ai/assist`, {
    method: "POST",
    headers: {"Authorization": `Bearer ${token}`, "Content-Type": "application/json"},
    body: JSON.stringify({prompt, context}),
  });
  if (!response.ok) {
    let message = `AI request failed (${response.status})`;
    try { const data = await response.json(); message = data?.detail ?? data?.error?.message ?? message; } catch {}
    throw new ApiError(message, response.status);
  }
  return (await response.json()) as AIAssistResponse;
}
