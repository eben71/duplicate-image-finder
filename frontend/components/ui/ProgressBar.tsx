export default function ProgressBar({ value }: { value: number }) {
  return (
    <div className="w-full h-1.5 rounded bg-[var(--color-ui-backgroundAlt)]" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.min(100, Math.max(0, value))} role="progressbar">
      <div
        className="h-1.5 rounded"
        style={{
          width: `${Math.min(100, Math.max(0, value))}%`,
          background: "linear-gradient(90deg, var(--color-primary-base), #56CCF2)"
        }}
      />
    </div>
  );
}
