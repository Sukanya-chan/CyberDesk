import { render, screen, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";
import * as authFetch from "../services/authFetch";

// Mock @clerk/react entirely: no real Clerk keys/network in unit tests.
// `mockSignedIn` is a module-level flag the tests below flip to switch
// which branch <Show when="..."> renders, mirroring how Clerk's own
// signed-in/out state would drive it at runtime.
let mockSignedIn = false;

vi.mock("@clerk/react", () => ({
  Show: ({ when, children }: { when: string; children: ReactNode }) => {
    if (when === "signed-in" && mockSignedIn) return <>{children}</>;
    if (when === "signed-out" && !mockSignedIn) return <>{children}</>;
    return null;
  },
  SignIn: () => <div>Clerk sign-in form</div>,
  SignUp: () => <div>Clerk sign-up form</div>,
  UserButton: () => <div>User menu</div>,
  useAuth: () => ({ getToken: vi.fn().mockResolvedValue("fake-token") }),
}));

describe("App shell (Phase 2 auth states)", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    mockSignedIn = false;
  });

  it("shows sign-in UI when signed out", () => {
    mockSignedIn = false;
    render(<App />);
    expect(screen.getByText(/clerk sign-in form/i)).toBeInTheDocument();
    expect(screen.queryByText(/clerk sign-up form/i)).not.toBeInTheDocument();
  });

  it("toggles to sign-up UI when signed out and the toggle is clicked", async () => {
    mockSignedIn = false;
    const { getByRole } = render(<App />);
    getByRole("button", { name: /new here\? sign up/i }).click();
    await waitFor(() => {
      expect(screen.getByText(/clerk sign-up form/i)).toBeInTheDocument();
    });
  });

  it("shows the authenticated account view when signed in, with the backend-assigned role", async () => {
    mockSignedIn = true;
    vi.spyOn(authFetch, "fetchCurrentUser").mockResolvedValue({
      id: 1,
      clerk_user_id: "user_test123",
      role: "student",
      created_at: "2026-01-01T00:00:00Z",
      updated_at: "2026-01-01T00:00:00Z",
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/role: student/i)).toBeInTheDocument();
    });
    expect(screen.queryByText(/clerk sign-in form/i)).not.toBeInTheDocument();
  });

  it("shows an error state when the backend rejects the authenticated request", async () => {
    mockSignedIn = true;
    vi.spyOn(authFetch, "fetchCurrentUser").mockRejectedValue(new Error("401"));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(/could not load account/i);
    });
  });
});
