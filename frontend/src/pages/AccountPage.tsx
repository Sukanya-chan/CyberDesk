import { useAuth, UserButton } from "@clerk/react";
import { useEffect, useState } from "react";

import { fetchCurrentUser } from "../services/authFetch";
import type { AppUser } from "../types/user";

type LoadState = "loading" | "success" | "error";

/**
 * Shown to signed-in users. Fetches /api/users/me to display the role the
 * BACKEND assigned — never a role read from Clerk or the frontend itself,
 * since the frontend is not a trusted source of authorization data.
 */
export function AccountPage() {
  const { getToken } = useAuth();
  const [state, setState] = useState<LoadState>("loading");
  const [user, setUser] = useState<AppUser | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    let cancelled = false;

    fetchCurrentUser(getToken)
      .then((data) => {
        if (cancelled) return;
        setUser(data);
        setState("success");
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        setErrorMessage(error instanceof Error ? error.message : "Unknown error");
        setState("error");
      });

    return () => {
      cancelled = true;
    };
  }, [getToken]);

  return (
    <main>
      <h1>CyberDesk</h1>
      <UserButton />

      {state === "loading" && <p role="status">Loading your account…</p>}
      {state === "error" && <p role="alert">Could not load account: {errorMessage}</p>}
      {state === "success" && user && (
        <ul>
          <li>Role: {user.role}</li>
          <li>Clerk user ID: {user.clerk_user_id}</li>
        </ul>
      )}
    </main>
  );
}
