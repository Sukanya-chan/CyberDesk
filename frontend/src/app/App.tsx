import { useState } from "react";

import { ProtectedRoute } from "../components/ProtectedRoute";
import { AccountPage } from "../pages/AccountPage";
import { SignInPage } from "../pages/SignInPage";
import { SignUpPage } from "../pages/SignUpPage";

/**
 * Application shell. Signed-out visitors see sign-in/sign-up (toggle);
 * signed-in visitors see the authenticated account view. See
 * ProtectedRoute for why this gating is UX-only, not a security control.
 */
export function App() {
  const [showSignUp, setShowSignUp] = useState(false);

  return (
    <ProtectedRoute
      fallback={
        <>
          {showSignUp ? <SignUpPage /> : <SignInPage />}
          <button type="button" onClick={() => setShowSignUp((prev) => !prev)}>
            {showSignUp ? "Already have an account? Sign in" : "New here? Sign up"}
          </button>
        </>
      }
    >
      <AccountPage />
    </ProtectedRoute>
  );
}
