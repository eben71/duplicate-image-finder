import { ButtonHTMLAttributes } from "react";
import clsx from "clsx";

type Variant = "primary" | "secondary" | "danger" | "ghost";
type Size = "sm" | "md" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
}

export default function Button({ variant = "primary", size = "md", className, ...props }: ButtonProps) {
  const base = "focus-ring inline-flex items-center justify-center rounded-[var(--radius-md)] transition disabled:opacity-50 disabled:cursor-not-allowed";
  const sizes = {
    sm: "px-[var(--space-sm)] h-8 text-[14px]",
    md: "px-[var(--space-lg)] h-10 text-[16px]",
    lg: "px-[var(--space-xl)] h-12 text-[16px]"
  }[size];
  const variants = {
    primary: "bg-[var(--color-primary-base)] text-white hover:bg-[var(--color-primary-hover)]",
    secondary: "border border-[var(--color-ui-border)] text-[var(--color-text-primary)] bg-transparent hover:bg-[var(--color-ui-backgroundAlt)]",
    danger: "bg-[var(--color-danger-base)] text-white",
    ghost: "bg-transparent text-[var(--color-text-primary)] hover:bg-[var(--color-ui-backgroundAlt)]"
  }[variant];
  return <button className={clsx(base, sizes, variants, className)} {...props} />;
}
