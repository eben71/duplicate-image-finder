import type { ReactNode } from "react";

interface BadgeProps {
  type: "keep" | "unsure" | "low";
  children?: ReactNode;
}

export default function Badge({ type, children }: BadgeProps) {
  const map = {
    keep: "bg-[var(--color-success-base)] text-white",
    unsure: "bg-[var(--color-warning-base)] text-black",
    low: "bg-[#BDBDBD] text-black"
  }[type];
  return (
    <span className={`inline-flex items-center px-[var(--space-xs)] py-0.5 rounded-full text-[12px] font-medium uppercase ${map}`}>
      {children}
    </span>
  );
}
