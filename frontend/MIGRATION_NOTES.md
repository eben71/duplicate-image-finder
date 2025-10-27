# Frontend migration notes

## Framework & tooling upgrades
- Upgraded to Next.js 15, React 19, and TypeScript 5.6 with strict bundler resolution.
- Standardized linting and formatting via ESLint 9 (Next config) and Prettier 3.
- Tailwind CSS 3.4, Storybook 8.2, Vitest 2, and Playwright 1.48 are now configured.
- Package manager is pinned to pnpm 9 with Node.js >= 20.10.0 engines.

## Code & configuration changes
- Regenerated `package.json` with new scripts (lint, typecheck, Storybook, Vitest, Playwright) and refreshed dependency versions.
- Added strict `tsconfig.json`, ESLint, Prettier, Tailwind, PostCSS, Vitest, and Playwright configs aligned with the new toolchain.
- Moved global styles to `app/globals.css`, updated the root layout to import it with React 19 type-safe props, and exposed a dashboard `<h1>` for accessibility and Playwright smoke coverage.
- Storybook configuration now targets `@storybook/nextjs` directly and reuses the shared Tailwind + theme provider styling.
- Added an initial Playwright smoke test under `e2e/` that validates the dashboard heading renders.

## Follow-ups
- Re-run `pnpm install` in an environment with registry access to materialize the new dependency tree.
- Once dependencies are installed, execute `pnpm run lint`, `pnpm run typecheck`, `pnpm run test`, and `pnpm run test:e2e` to confirm no latent runtime issues.
- Consider adopting `@storybook/test` in any bespoke testing utilities if future work integrates Storybook stories with Vitest/Playwright.

## CI recommendations
- Ensure CI workflows use Node.js 20.x (>= 20.10.0) and `pnpm/action-setup@v4` to install pnpm 9 before building or testing the frontend.
