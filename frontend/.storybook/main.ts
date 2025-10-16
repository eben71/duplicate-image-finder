import type { StorybookConfig } from "@storybook/nextjs";
import path from "path";

const config: StorybookConfig = {
  stories: ["../components/**/*.stories.@(ts|tsx)", "../app/**/*.stories.@(ts|tsx)"],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y"
  ],
  framework: {
    name: "@storybook/nextjs",
    options: {}
  },
  docs: {
    autodocs: "tag"
  },
  webpackFinal: async (config) => {
    if (config.resolve) {
      config.resolve.alias = {
        ...(config.resolve.alias || {}),
        "@ui": path.resolve(__dirname, "../components/ui"),
        "@layout": path.resolve(__dirname, "../components/layout"),
        "@review": path.resolve(__dirname, "../components/review"),
        "@theme": path.resolve(__dirname, "../theme"),
        "@lib": path.resolve(__dirname, "../lib")
      };
    }
    return config;
  }
};

export default config;
