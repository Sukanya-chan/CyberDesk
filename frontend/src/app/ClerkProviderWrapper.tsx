import { ClerkProvider } from "@clerk/react";
import type { ReactNode } from "react";

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error(
    "Missing VITE_CLERK_PUBLISHABLE_KEY. Copy frontend/.env.example to " +
      "frontend/.env and add your Clerk publishable key.",
  );
}

/**
 * Wraps the app with Clerk's session/user context. The publishable key is
 * safe to expose in the browser bundle — it identifies the Clerk
 * application, not a secret. The Clerk secret key must never appear here
 * or anywhere in frontend code.
 */
export function ClerkProviderWrapper({ children }: { children: ReactNode }) {
  return <ClerkProvider publishableKey={PUBLISHABLE_KEY}>{children}</ClerkProvider>;
}
