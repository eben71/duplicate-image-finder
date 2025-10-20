import Card from "@ui/Card";
import Button from "@ui/Button";

export default function Help() {
  return (
    <section className="space-y-4">
      <header>
        <h1 className="text-xl font-semibold">Help & Feedback</h1>
        <p className="text-[14px] text-[var(--color-text-secondary)]">Tell us how to improve duplicate reviews.</p>
      </header>
      <Card>
        <div className="flex flex-col gap-3">
          <div>
            <h2 className="text-lg font-semibold">Need assistance?</h2>
            <p className="text-[14px] text-[var(--color-text-secondary)]">Check our docs or send product feedback.</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button variant="secondary">Open Docs</Button>
            <Button variant="ghost">Contact Support</Button>
          </div>
        </div>
      </Card>
    </section>
  );
}
