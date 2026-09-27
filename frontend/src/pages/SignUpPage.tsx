import { SignUp } from "@clerk/react";

/**
 * Clerk's prebuilt sign-up UI. Every new student who signs up gets a
 * CyberDesk AppUser row lazily created (role: "student") the first time
 * they call an authenticated backend endpoint — see ADR-008.
 */
export function SignUpPage() {
  return (
    <main>
      <h1>Create your CyberDesk account</h1>
      <SignUp />
    </main>
  );
}
