import Card from "@ui/Card";
import Badge from "@ui/Badge";
import Button from "@ui/Button";

interface GroupCardProps {
  id: string;
  count: number;
  range: string;
  badge: { type: "keep" | "unsure" | "low"; text: string };
  onOpen: () => void;
}

export default function GroupCard({ id, count, range, badge, onOpen }: GroupCardProps) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="font-medium">Group #{id}</div>
          <div className="text-[14px] text-[var(--color-text-secondary)] mt-1">
            {count} photos • {range} match
          </div>
        </div>
        <Badge type={badge.type}>{badge.text}</Badge>
      </div>
      <div className="mt-4 flex items-center justify-between gap-2">
        <Button size="sm" onClick={onOpen} className="w-full md:w-auto">
          Review Group →
        </Button>
        <span className="hidden md:inline text-[12px] text-[var(--color-text-secondary)]">AI recommends what to keep.</span>
      </div>
    </Card>
  );
}
