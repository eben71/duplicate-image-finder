import { Table, THead, TRow } from "@ui/Table";

const rows = [
  { group: "#203", action: "3 Deleted, 3 Kept", confidence: "95%", date: "13 Oct 2025", link: "View in Trash" },
  { group: "#204", action: "1 Deleted, 3 Kept", confidence: "88%", date: "12 Oct 2025", link: "View" },
  { group: "#205", action: "2 Archived", confidence: "72%", date: "10 Oct 2025", link: "Google Photos" }
];

export default function Activity() {
  return (
    <section className="space-y-4">
      <header>
        <h1 className="text-xl font-semibold">Activity log</h1>
        <p className="text-[14px] text-[var(--color-text-secondary)]">Audit every decision synced to Google Photos Trash.</p>
      </header>
      <Table role="table">
        <THead>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-2">
            <span>Group</span>
            <span className="hidden md:block">Action</span>
            <span className="hidden md:block">Confidence</span>
            <span className="hidden md:block">Date</span>
            <span className="hidden md:block">Links</span>
          </div>
        </THead>
        {rows.map((row) => (
          <TRow key={row.group}>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-2 text-[14px]">
              <span>{row.group}</span>
              <span>{row.action}</span>
              <span className="hidden md:block">{row.confidence}</span>
              <span className="hidden md:block">{row.date}</span>
              <button type="button" className="focus-ring text-left text-[var(--color-primary-base)]">
                {row.link}
              </button>
            </div>
          </TRow>
        ))}
      </Table>
    </section>
  );
}
