import type { Preview } from "@storybook/react";
import ThemeProvider from "../theme/ThemeProvider";
import "../app/globals.css";

const preview: Preview = {
  parameters: {
    controls: { expanded: true }
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
