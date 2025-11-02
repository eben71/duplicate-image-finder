/**
 * Minimal Next.js configuration used exclusively for Storybook.
 * Keeping this separate avoids pulling in project-specific
 * Turbopack options that the Storybook webpack builder cannot
 * interpret.
 */
const config = {
  experimental: {
    appDir: false
  },
  images: {
    unoptimized: true
  }
};

module.exports = config;
