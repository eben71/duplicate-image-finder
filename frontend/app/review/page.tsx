"use client";
import { useRouter } from "next/navigation";
import { groups } from "@lib/mockData";
import GroupCard from "@review/GroupCard";

export default function ReviewList() {
  const router = useRouter();
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-semibold">Review duplicate groups</h1>
        <p className="text-[14px] text-[var(--color-text-secondary)]">
          AI recommends what to keep. You confirm every delete.
        </p>
      </div>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {groups.map((group) => (
          <GroupCard
            key={group.id}
            id={group.id}
            count={group.count}
            range={group.sim}
            badge={group.ai}
            onOpen={() => router.push(`/review/${group.id}`)}
          />
        ))}
      </div>
    </div>
  );
}
