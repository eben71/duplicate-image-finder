import Card from "@ui/Card";
import Button from "@ui/Button";

export default function Settings() {
  return (
    <section className="space-y-4">
      <header>
        <h1 className="text-xl font-semibold">Settings</h1>
        <p className="text-[14px] text-[var(--color-text-secondary)]">Account controls are coming soon.</p>
      </header>
      <Card>
        <div className="flex flex-col gap-3">
          <div>
            <h2 className="text-lg font-semibold">Plan</h2>
            <p className="text-[14px] text-[var(--color-text-secondary)]">Upgrade for unlimited scans and faster AI suggestions.</p>
          </div>
          <Button>View Plans</Button>
        </div>
      </Card>
    </section>
  );
}
