/**
 * Typed fetch wrapper for all backend API calls.
 * Base URL is read from NEXT_PUBLIC_API_URL (set in .env.local).
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export type ServiceState = "ok" | "error";

export interface ServiceStatuses {
  postgres: ServiceState;
  mongodb: ServiceState;
  qdrant: ServiceState;
  gemini: ServiceState;
}

export interface HealthResponse {
  status: "ok" | "degraded";
  services: ServiceStatuses;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/health`, {
    // No caching — this must be a live check every time
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Health endpoint returned HTTP ${res.status}`);
  }

  return res.json() as Promise<HealthResponse>;
}
