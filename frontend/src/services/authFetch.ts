/**
 * Authenticated API calls to the CyberDesk backend.
 *
 * `getToken` is `useAuth().getToken` from `@clerk/react` — passed in by
 * the caller (a component) rather than imported here, since this module
 * is plain TS and Clerk's hooks can only be called from React components.
 */
import { ApiError } from "./api";
import type { AppUser } from "../types/user";

const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

type GetToken = () => Promise<string | null>;

async function authedFetch(path: string, getToken: GetToken): Promise<Response> {
  const token = await getToken();
  if (!token) {
    throw new ApiError("Not signed in", 401);
  }

  return fetch(`${API_BASE_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function fetchCurrentUser(getToken: GetToken): Promise<AppUser> {
  const response = await authedFetch("/users/me", getToken);

  if (!response.ok) {
    throw new ApiError(`Failed to load current user (${response.status})`, response.status);
  }

  return (await response.json()) as AppUser;
}

export async function fetchAdminPing(getToken: GetToken): Promise<{ message: string; role: string }> {
  const response = await authedFetch("/admin/ping", getToken);

  if (!response.ok) {
    throw new ApiError(`Admin ping failed (${response.status})`, response.status);
  }

  return await response.json();
}
