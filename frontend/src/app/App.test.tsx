import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";
import * as api from "../services/api";

describe("App shell", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders the loading state, then shows backend health on success", async () => {
    vi.spyOn(api, "fetchHealth").mockResolvedValue({
      status: "ok",
      service: "CyberDesk API",
      environment: "development",
      database: "ok",
    });

    render(<App />);

    expect(screen.getByRole("status")).toHaveTextContent(/checking backend status/i);

    await waitFor(() => {
      expect(screen.getByText(/status: ok/i)).toBeInTheDocument();
    });
  });

  it("shows an error state when the backend is unreachable", async () => {
    vi.spyOn(api, "fetchHealth").mockRejectedValue(new Error("network error"));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(/could not reach backend/i);
    });
  });
});
