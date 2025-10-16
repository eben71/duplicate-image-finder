import type { Preview } from "@storybook/react";
import React from "react";
import ThemeProvider from "../theme/ThemeProvider";
import "../styles/globals.css";

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/
      }
    },
    backgrounds: {
      default: "app",
      values: [
        { name: "app", value: "var(--color-ui-background)" },
        { name: "alt", value: "var(--color-ui-backgroundAlt)" }
      ]
    }
  },
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="min-h-screen bg-[var(--color-ui-background)] text-[var(--color-text-primary)] p-[var(--space-lg)]">
          <Story />
        </div>
      </ThemeProvider>
    )
  ]
};

export default preview;
