"use client";
import { useState } from "react";
import ComparePanel from "@review/ComparePanel";
import ActionBar from "@layout/ActionBar";
import Filmstrip from "@review/Filmstrip";
import { groupThumbnails } from "@lib/mockData";
import { keys } from "@lib/keyboard";

export default function GroupDetail() {
  const [activeId, setActiveId] = useState<string>(groupThumbnails[0]?.id ?? "");

  return (
    <div className="grid gap-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-semibold">Group #203</h1>
        <p className="text-[14px] text-[var(--color-text-secondary)]">
          6 photos • Similarity 94–98%. AI suggests keeping the sharpest thumbnail. No deletions happen until you confirm.
        </p>
        <div className="flex flex-wrap gap-4 text-[12px] text-[var(--color-text-secondary)]" role="note">
          <span>Keyboard: Keep ({keys.Keep.toUpperCase()})</span>
          <span>Skip ({keys.Skip.toUpperCase()})</span>
          <span>Flag delete for review ({keys.Delete.toUpperCase()})</span>
        </div>
      </div>

      <Filmstrip items={groupThumbnails} onSelect={setActiveId} activeId={activeId} />
      <ComparePanel />
      <ActionBar onKeepBest={() => {}} onManual={() => {}} onSkip={() => {}} />
    </div>
  );
}
