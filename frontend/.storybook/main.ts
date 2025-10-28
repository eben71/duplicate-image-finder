import type { StorybookConfig } from "@storybook/nextjs";
import path from "node:path";
import react from "@vitejs/plugin-react";

const config: StorybookConfig = {
  framework: {
    name: "@storybook/nextjs",
    options: {
      builder: {
        name: "@storybook/builder-vite"
      }
    }
  },
  core: {
    builder: "@storybook/builder-vite"
  },
  stories: ["../components/**/*.stories.@(ts|tsx)", "../app/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-essentials", "@storybook/addon-interactions", "@storybook/addon-a11y"],
  viteFinal: async (config, { configType }) => {
    config.plugins = config.plugins || [];
    config.plugins.push(
      react({
        jsxRuntime: "automatic",
        jsxImportSource: undefined
      })
    );
    config.resolve = config.resolve || {};
    const alias = Array.isArray(config.resolve.alias) ? {} : config.resolve.alias || {};
    Object.assign(alias, {
      "@ui": path.resolve(__dirname, "../components/ui"),
      "@layout": path.resolve(__dirname, "../components/layout"),
      "@review": path.resolve(__dirname, "../components/review"),
      "@theme": path.resolve(__dirname, "../theme"),
      "@lib": path.resolve(__dirname, "../lib")
    });
    config.resolve.alias = alias;
    config.define = {
      ...(config.define || {}),
      "process.env": config.define?.["process.env"] ?? "{}"
    };
    if (configType === "PRODUCTION") {
      config.build = config.build || {};
      config.build.minify = config.build.minify ?? "esbuild";
    }
    return config;
  }
};

export default config;
