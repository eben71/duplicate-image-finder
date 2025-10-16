import type { ReactNode } from "react";

interface TableProps {
  children: ReactNode;
  role?: "table" | "presentation";
}
export function Table({ children, role = "table" }: TableProps) {
  return (
    <div className="border border-[var(--color-ui-border)] rounded-[var(--radius-md)] overflow-hidden" role={role}>
      {children}
    </div>
  );
}
export function THead({ children }: { children: ReactNode }) {
  return <div className="grid bg-[var(--color-ui-backgroundAlt)] text-[14px] font-semibold p-[var(--space-md)]">{children}</div>;
}
export function TRow({ children }: { children: ReactNode }) {
  return (
    <div className="grid border-t border-[var(--color-ui-border)] p-[var(--space-md)] hover:bg-[var(--color-ui-backgroundAlt)] focus-within:bg-[var(--color-ui-backgroundAlt)]">
      {children}
    </div>
  );
}
