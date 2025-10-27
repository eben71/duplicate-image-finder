import Card from "@ui/Card";
import ProgressBar from "@ui/ProgressBar";
import Button from "@ui/Button";
import { formatNumber } from "@lib/formatters";

export default function Dashboard() {
  return (
    <div className="grid gap-6">
      <h1 className="text-3xl font-semibold">Duplicate Image Finder</h1>
      <div className="grid md:grid-cols-3 gap-4">
        <Card>
          <div className="text-sm text-[var(--color-text-secondary)]">Photos Scanned</div>
          <div className="text-2xl font-semibold mt-2">{formatNumber(12480)}</div>
        </Card>
        <Card>
          <div className="text-sm text-[var(--color-text-secondary)]">Groups Found</div>
          <div className="text-2xl font-semibold mt-2">{formatNumber(312)}</div>
        </Card>
        <Card>
          <div className="text-sm text-[var(--color-text-secondary)]">Space Saved</div>
          <div className="text-2xl font-semibold mt-2">1.2 GB</div>
        </Card>
      </div>
      <Card>
        <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div className="font-medium">Current Scan</div>
          <label className="flex items-center gap-2 text-[14px]">
            <span className="text-[var(--color-text-secondary)]">Mode</span>
            <select className="focus-ring border border-[var(--color-ui-border)] rounded px-2 py-1 bg-white">
              <option>Full Library</option>
              <option>New Photos Only</option>
              <option>New vs All</option>
            </select>
          </label>
        </div>
        <ProgressBar value={80} />
        <div className="flex flex-wrap gap-2 mt-3">
          <Button variant="secondary">Pause</Button>
          <Button variant="ghost">Stop</Button>
        </div>
        <p className="mt-3 text-[12px] text-[var(--color-text-secondary)]">
          Mobile control: you can pause or stop scans from any device. Library changes remain review-only until confirmed on desktop.
        </p>
      </Card>
      <Card>
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="font-medium">Ready to start reviewing?</div>
            <div className="text-[14px] text-[var(--color-text-secondary)]">
              AI suggests which to keep — you make the final call. Nothing is deleted automatically.
            </div>
          </div>
          <Button>Start Reviewing</Button>
        </div>
      </Card>
    </div>
  );
}
