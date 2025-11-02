// Minimal ambient type declarations to satisfy Vitest's dependency on `vite/client`.
// These definitions cover the parts of the Vite runtime API that our tests rely on
// (primarily `import.meta.env` and `import.meta.glob` helpers) without pulling in the
// full Vite package as a dev dependency.

type ViteGlobImportOptions = {
  eager?: boolean;
  import?: string;
  as?: string;
  query?: Record<string, string | number | boolean>;
};

type ViteGlobResult<T = unknown> = Record<string, T>;

type ViteGlobFunction = <T = unknown>(
  pattern: string,
  options?: ViteGlobImportOptions
) => ViteGlobResult<T>;

declare interface ImportMetaEnv {
  readonly [key: string]: string | boolean | number | undefined;
}

declare interface ImportMeta {
  readonly env: ImportMetaEnv;
  glob: ViteGlobFunction;
  globEager: ViteGlobFunction;
  globEagerDefault: ViteGlobFunction;
}

declare module 'vite/client' {
  export {};
}
