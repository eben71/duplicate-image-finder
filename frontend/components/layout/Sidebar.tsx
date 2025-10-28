"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const items = [
  { href: "/", label: "Dashboard" },
  { href: "/review", label: "Review Groups" },
  { href: "/activity", label: "Activity Log" },
  { href: "/settings", label: "Settings" },
  { href: "/help", label: "Help / Feedback" }
];
export default function Sidebar() {
  const pathname = usePathname() ?? "/";

  return (
    <aside className="hidden md:flex md:w-60 flex-col gap-1 p-4 bg-[var(--color-ui-backgroundAlt)] min-h-screen" aria-label="Primary">
      {items.map((item) => {
        const active = pathname === item.href || pathname.startsWith(item.href + "/");
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`rounded px-3 py-2 hover:bg-white border border-transparent hover:border-[var(--color-ui-border)] focus-ring ${active ? "bg-white border-[var(--color-ui-border)]" : ""}`}
            aria-current={active ? "page" : undefined}
          >
            {item.label}
          </Link>
        );
      })}
    </aside>
  );
}
