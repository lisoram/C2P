import type { ServiceState } from "@/lib/api";

interface Props {
  name: string;
  state: ServiceState | "loading" | "fetch-error";
}

const labels: Record<string, string> = {
  postgres: "PostgreSQL",
  mongodb: "MongoDB",
  qdrant: "Qdrant",
  gemini: "Gemini API",
};

const badge: Record<string, { bg: string; text: string; dot: string; label: string }> = {
  ok: {
    bg: "bg-green-50 border-green-200",
    text: "text-green-800",
    dot: "bg-green-500",
    label: "Connected",
  },
  error: {
    bg: "bg-red-50 border-red-200",
    text: "text-red-800",
    dot: "bg-red-500",
    label: "Unreachable",
  },
  loading: {
    bg: "bg-gray-50 border-gray-200",
    text: "text-gray-500",
    dot: "bg-gray-400 animate-pulse",
    label: "Checking…",
  },
  "fetch-error": {
    bg: "bg-yellow-50 border-yellow-200",
    text: "text-yellow-800",
    dot: "bg-yellow-500",
    label: "Backend unreachable",
  },
};

export default function ServiceStatus({ name, state }: Props) {
  const style = badge[state] ?? badge["loading"];
  const displayName = labels[name] ?? name;

  return (
    <div
      className={`flex items-center justify-between rounded-lg border px-4 py-3 ${style.bg}`}
    >
      <span className={`text-sm font-medium ${style.text}`}>{displayName}</span>
      <span className={`flex items-center gap-2 text-sm ${style.text}`}>
        <span className={`inline-block h-2 w-2 rounded-full ${style.dot}`} />
        {style.label}
      </span>
    </div>
  );
}
