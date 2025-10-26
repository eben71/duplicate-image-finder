import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    globals: true,
    css: true,
    coverage: {
      reporter: ["text", "json", "json-summary", "lcov", "html"],
      reportsDirectory: "../coverage/frontend",
      include: ["components/**/*.{ts,tsx}", "app/**/*.{ts,tsx}"]
    }
  }
});
