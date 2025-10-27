import type { StorybookConfig } from "@storybook/nextjs";
import path from "path";

const config: StorybookConfig = {
  framework: "@storybook/nextjs",
  stories: ["../components/**/*.stories.@(ts|tsx)", "../app/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-essentials", "@storybook/addon-interactions", "@storybook/addon-a11y"],
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
