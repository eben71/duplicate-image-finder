import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./pages/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "var(--color-primary-base)",
          hover: "var(--color-primary-hover)"
        },
        success: "var(--color-success-base)",
        warning: "var(--color-warning-base)",
        danger: "var(--color-danger-base)",
        border: "var(--color-ui-border)",
        bg: "var(--color-ui-background)",
        bgAlt: "var(--color-ui-backgroundAlt)"
      },
      borderRadius: {
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)"
      },
      fontFamily: {
        sans: "var(--font-family-base)",
        heading: "var(--font-family-heading)",
        mono: "var(--font-family-mono)"
      }
    }
  },
  plugins: []
};

export default config;
