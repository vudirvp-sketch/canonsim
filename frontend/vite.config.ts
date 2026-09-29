/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The dev-server proxy: the browser client stays same-origin to the
// Vite dev server, which forwards /gateway/* to the Python loopback
// gateway (default bind 127.0.0.1:8765 — scripts/workbench_app.py's
// DEFAULT_PORT). This is CLIENT-side dev tooling only: the gateway
// itself is untouched (no CORS surface added to the backend; the
// production serving path is a post-S0 concern).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/gateway": {
        target: process.env["GATEWAY_TARGET"] ?? "http://127.0.0.1:8765",
        changeOrigin: false,
        rewrite: (path) => path.replace(/^\/gateway/, ""),
      },
    },
  },
  test: {
    environment: "jsdom",
    globals: false,
    include: ["tests/**/*.test.{ts,tsx}"],
  },
});
