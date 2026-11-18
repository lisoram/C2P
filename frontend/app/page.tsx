/**
 * Home page – live backend health dashboard.
 *
 * This is a Next.js Server Component (the default).
 * It fetches /api/v1/health on every request (cache: "no-store" in lib/api.ts)
 * so the status is always live, not cached.
 *
 * If the backend is unreachable, every service shows "fetch-error"
 * rather than crashing the page.
 */

import ServiceStatus from "@/components/ServiceStatus";
import { fetchHealth, type ServiceStatuses } from "@/lib/api";

const SERVICE_KEYS: (keyof ServiceStatuses)[] = [
  "postgres",
  "mongodb",
  "qdrant",
  "gemini",
];

export default async function HomePage() {
  let data: Awaited<ReturnType<typeof fetchHealth>> | null = null;
  let fetchFailed = false;

  try {
    data = await fetchHealth();
  } catch {
    fetchFailed = true;
  }

  const overallOk = !fetchFailed && data?.status === "ok";

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-2xl font-bold text-slate-900">C2P — System Status</h1>
          <p className="mt-1 text-sm text-slate-500">Module 0 — Infrastructure health</p>
        </div>

        {/* Overall banner */}
        <div
          className={`rounded-xl border-2 p-4 text-center font-semibold ${
            fetchFailed
              ? "border-yellow-400 bg-yellow-50 text-yellow-800"
              : overallOk
              ? "border-green-400 bg-green-50 text-green-800"
              : "border-red-400 bg-red-50 text-red-800"
          }`}
        >
          {fetchFailed
            ? "⚠ Cannot reach backend"
            : overallOk
            ? "✓ All systems operational"
            : "✗ One or more services degraded"}
        </div>

        {/* Per-service rows */}
        <div className="space-y-3">
          {SERVICE_KEYS.map((key) => (
            <ServiceStatus
              key={key}
              name={key}
              state={
                fetchFailed
                  ? "fetch-error"
                  : data
                  ? data.services[key]
                  : "loading"
              }
            />
          ))}
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-slate-400">
          Fetched at {new Date().toLocaleTimeString("en-IN", { timeZone: "Asia/Kolkata" })} IST
        </p>
      </div>
    </main>
  );
}
