/**
 * Minimal API client for talking to the CyberDesk backend.
 * The base URL is read from the environment (see .env.example) so it
 * can change between local development and later deployment targets.
 */

const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export interface HealthResponse {
  status: string;
  service: string;
  environment: string;
  database: string;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new ApiError(`Health check failed with status ${response.status}`, response.status);
  }

  return (await response.json()) as HealthResponse;
}
