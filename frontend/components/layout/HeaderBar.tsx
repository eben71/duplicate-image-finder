import Image from "next/image";
import Link from "next/link";

export default function HeaderBar() {
  return (
    <header className="sticky top-0 z-40 border-b border-[var(--color-ui-border)] bg-[var(--color-ui-background)]">
      <div className="container-max px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/" className="focus-ring flex items-center gap-2 font-heading text-lg">
            <Image src="/logo.svg" alt="Duplicate Image Finder" width={24} height={24} />
            <span>Duplicate Image Finder</span>
          </Link>
          <span className="hidden md:inline text-xs text-[var(--color-text-secondary)]">AI suggests keeps — you stay in control.</span>
        </div>
        <div className="text-sm text-[var(--color-text-secondary)] flex items-center gap-2">
          <span>Plan: Free</span>
          <Link href="/settings" className="focus-ring text-[var(--color-primary-base)]">Upgrade</Link>
        </div>
      </div>
    </header>
  );
}
