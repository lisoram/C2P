import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow the backend URL to be configured via environment variable.
  // In development this is typically http://localhost:8000.
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  },
};

export default nextConfig;
