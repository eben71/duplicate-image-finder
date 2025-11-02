// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  turbopack: {
    root: __dirname, // points to /frontend
  },
};

export default nextConfig;
