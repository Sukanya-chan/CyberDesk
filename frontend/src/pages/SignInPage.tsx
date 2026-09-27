import { SignIn } from "@clerk/react";

/**
 * Clerk's prebuilt sign-in UI. CyberDesk never sees or handles a
 * password — Clerk collects credentials directly.
 */
export function SignInPage() {
  return (
    <main>
      <h1>Sign in to CyberDesk</h1>
      <SignIn />
    </main>
  );
}
