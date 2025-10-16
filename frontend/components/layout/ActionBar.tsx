import Button from "@ui/Button";

interface ActionBarProps {
  onKeepBest: () => void;
  onManual: () => void;
  onSkip: () => void;
  disabled?: boolean;
}

export default function ActionBar({ onKeepBest, onManual, onSkip, disabled }: ActionBarProps) {
  return (
    <div className="sticky bottom-0 border-t border-[var(--color-ui-border)] bg-[var(--color-ui-background)] hidden md:block" aria-label="Review actions">
      <div className="container-max px-4 py-3 flex flex-wrap items-center gap-3">
        <Button onClick={onKeepBest} disabled={disabled} aria-disabled={disabled}>
          Keep Best + Delete Others
        </Button>
        <Button variant="secondary" onClick={onManual} disabled={disabled} aria-disabled={disabled}>
          Select Keeps Manually
        </Button>
        <Button variant="ghost" onClick={onSkip}>
          Skip Group
        </Button>
        <div className="ml-auto text-[14px] text-[var(--color-text-secondary)]">
          No photos are deleted automatically.
        </div>
      </div>
    </div>
  );
}
