"use client";
import React, { PropsWithChildren, useMemo } from "react";
import tokens from "./tokens.json";

function applyVars(root: HTMLElement, obj: any, prefix: string[] = []) {
  Object.entries(obj).forEach(([k, v]) => {
    const path = [...prefix, k];
    if (v && typeof v === "object" && !Array.isArray(v)) {
      applyVars(root, v, path);
    } else {
      const name = `--${path.join("-")}`;
      root.style.setProperty(name, String(v));
    }
  });
}

export default function ThemeProvider({ children }: PropsWithChildren) {
  useMemo(() => {
    if (typeof window !== "undefined") {
      applyVars(document.documentElement, tokens);
      document.documentElement.style.setProperty("--app-max-width", "1200px");
    }
  }, []);
  return <>{children}</>;
}
