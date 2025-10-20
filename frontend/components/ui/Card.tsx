import type { ReactNode } from "react";

export default function Card({ children }: { children: ReactNode }) {
  return <div className="card p-[var(--space-lg)]">{children}</div>;
}
