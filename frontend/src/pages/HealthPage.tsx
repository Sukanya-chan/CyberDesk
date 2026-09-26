import { useEffect, useState } from "react";

import { fetchHealth, type HealthResponse } from "../services/api";

type LoadState = "loading" | "success" | "error" | "empty";

export function HealthPage() {
  const [state, setState] = useState<LoadState>("loading");
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    let cancelled = false;

    fetchHealth()
      .then((data) => {
        if (cancelled) return;
        if (!data) {
          setState("empty");
          return;
        }
        setHealth(data);
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
  }, []);

  return (
    <main>
      <h1>CyberDesk</h1>
      <p>Backend connectivity check</p>

      {state === "loading" && <p role="status">Checking backend status…</p>}

      {state === "error" && (
        <p role="alert">Could not reach backend: {errorMessage}</p>
      )}

      {state === "empty" && <p>No health data returned.</p>}

      {state === "success" && health && (
        <ul>
          <li>Status: {health.status}</li>
          <li>Service: {health.service}</li>
          <li>Environment: {health.environment}</li>
          <li>Database: {health.database}</li>
        </ul>
      )}
    </main>
  );
}
