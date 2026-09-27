import { Show } from "@clerk/react";
import type { ReactNode } from "react";

/**
 * Gates its children on Clerk's client-side signed-in state.
 *
 * IMPORTANT: this is a UX convenience only, not a security boundary.
 * Hiding a component here does not authorize anything — every protected
 * backend endpoint independently re-verifies the request and checks the
 * caller's role. See specs/Security.md and context/Decisions.md.
 */
export function ProtectedRoute({
  children,
  fallback,
}: {
  children: ReactNode;
  fallback: ReactNode;
}) {
  return (
    <>
      <Show when="signed-in">{children}</Show>
      <Show when="signed-out">{fallback}</Show>
    </>
  );
}
