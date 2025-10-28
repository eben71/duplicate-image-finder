import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  plugins: [
    react({
      jsxRuntime: "automatic"
    })
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "."),
      "@ui": path.resolve(__dirname, "components/ui"),
      "@layout": path.resolve(__dirname, "components/layout"),
      "@review": path.resolve(__dirname, "components/review"),
      "@theme": path.resolve(__dirname, "theme"),
      "@lib": path.resolve(__dirname, "lib")
    }
  },
  test: {
    environment: "jsdom",
    environmentOptions: {
      jsdom: {
        url: "http://localhost"
      }
    },
    exclude: ["node_modules", "dist", ".next", "e2e/**/*"],
    setupFiles: ["./vitest.setup.ts"],
    globals: true,
    css: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      include: ["**/*.{ts,tsx}"]
    }
  }
});
