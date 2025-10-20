"use client";
import { useEffect, useMemo, useState } from "react";
import clsx from "clsx";

const SAMPLE_IMAGES = [
  {
    id: "1",
    thumbnail: "linear-gradient(135deg, #2F80ED 0%, #56CCF2 100%)",
    alt: "Sunset skyline thumbnail",
    filename: "IMG_2031.JPG",
    capture: "13 Oct 2025 • 4.2 MB",
    aiKeep: true
  },
  {
    id: "2",
    thumbnail: "linear-gradient(135deg, #EB5757 0%, #F2994A 100%)",
    alt: "Sunset variation thumbnail",
    filename: "IMG_2032.JPG",
    capture: "13 Oct 2025 • 4.1 MB",
    aiKeep: false
  },
  {
    id: "3",
    thumbnail: "linear-gradient(135deg, #27AE60 0%, #6FCF97 100%)",
    alt: "Forest ridge thumbnail",
    filename: "IMG_2033.JPG",
    capture: "13 Oct 2025 • 3.9 MB",
    aiKeep: false
  },
  {
    id: "4",
    thumbnail: "linear-gradient(135deg, #BB6BD9 0%, #56CCF2 100%)",
    alt: "Forest ridge variant thumbnail",
    filename: "IMG_2034.JPG",
    capture: "13 Oct 2025 • 3.8 MB",
    aiKeep: false
  },
  {
    id: "5",
    thumbnail: "linear-gradient(135deg, #9B51E0 0%, #F2C94C 100%)",
    alt: "Portrait duplicate thumbnail",
    filename: "IMG_2035.JPG",
    capture: "13 Oct 2025 • 3.8 MB",
    aiKeep: false
  },
  {
    id: "6",
    thumbnail: "linear-gradient(135deg, #56CCF2 0%, #2F80ED 100%)",
    alt: "Portrait variation thumbnail",
    filename: "IMG_2036.JPG",
    capture: "13 Oct 2025 • 3.7 MB",
    aiKeep: false
  }
];

type Mode = 2 | 4 | 8;

export default function ComparePanel() {
  const [mode, setMode] = useState<Mode>(2);
  const [keeps, setKeeps] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    SAMPLE_IMAGES.forEach((image) => {
      initial[image.id] = image.aiKeep;
    });
    return initial;
  });
  const [isMobile, setIsMobile] = useState<boolean>(false);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const update = () => setIsMobile(window.innerWidth < 768);
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  const visibleImages = useMemo(() => SAMPLE_IMAGES.slice(0, mode), [mode]);
  const columnClass = useMemo(() => {
    if (mode === 2) return "md:grid-cols-2";
    if (mode === 4) return "md:grid-cols-4";
    return "md:grid-cols-4";
  }, [mode]);

  const instructions = useMemo(() => {
    if (mode === 2) return "2-up";
    if (mode === 4) return "4-up";
    return "8-up";
  }, [mode]);

  const toggleKeep = (id: string) => {
    if (isMobile) return;
    setKeeps((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="font-medium">Review comparison</div>
          <p className="text-[14px] text-[var(--color-text-secondary)]">Mode: {instructions} • AI suggests keep only — confirm before deleting.</p>
        </div>
        <div role="radiogroup" aria-label="Change comparison layout" className="inline-flex rounded-[var(--radius-md)] border border-[var(--color-ui-border)] overflow-hidden">
          {[2, 4, 8].map((value) => (
            <button
              key={value}
              type="button"
              role="radio"
              aria-checked={mode === value}
              onClick={() => setMode(value as Mode)}
              className={clsx(
                "focus-ring px-[var(--space-md)] py-2 text-[14px] transition",
                mode === value ? "bg-[var(--color-primary-base)] text-white" : "bg-transparent text-[var(--color-text-primary)]"
              )}
            >
              {value}-up
            </button>
          ))}
        </div>
      </div>

      {isMobile && (
        <div className="rounded-[var(--radius-md)] border border-dashed border-[var(--color-ui-border)] bg-[var(--color-ui-backgroundAlt)] p-[var(--space-lg)] text-[14px] text-[var(--color-text-secondary)]">
          Reviewing groups is desktop-only. You can preview thumbnails here, but changes must be confirmed on a larger screen.
        </div>
      )}

      <div className={clsx("grid gap-4", columnClass, mode === 8 ? "md:grid-rows-2" : "")}
        aria-live="polite"
        aria-label={`Showing ${instructions} comparison`}
      >
        {visibleImages.map((image) => {
          const checked = keeps[image.id];
          return (
            <figure key={image.id} className="group relative flex flex-col overflow-hidden rounded-[var(--radius-md)] border border-[var(--color-ui-border)] bg-[var(--color-ui-background)] shadow-sm">
              <div
                className="relative aspect-[4/3] w-full bg-[var(--color-ui-backgroundAlt)]"
                role="img"
                aria-label={image.alt}
                style={{ backgroundImage: image.thumbnail, backgroundSize: "cover", backgroundPosition: "center" }}
              >
                {image.aiKeep && (
                  <span className="absolute left-2 top-2 rounded-full bg-black/65 px-2 py-1 text-[12px] text-white">AI suggests keep</span>
                )}
              </div>
              <figcaption className="flex flex-col gap-1 p-[var(--space-md)] text-[14px]">
                <span className="font-medium text-[var(--color-text-primary)]">{image.filename}</span>
                <span className="text-[var(--color-text-secondary)]">{image.capture}</span>
                <label className="mt-2 inline-flex items-center gap-2 text-[14px]">
                  <input
                    type="checkbox"
                    className="h-4 w-4 rounded border-[var(--color-ui-border)] text-[var(--color-primary-base)]"
                    checked={checked}
                    onChange={() => toggleKeep(image.id)}
                    disabled={isMobile}
                    aria-describedby={isMobile ? "mobile-readonly" : undefined}
                  />
                  <span>{checked ? "Keep selected" : "Mark to keep"}</span>
                </label>
              </figcaption>
            </figure>
          );
        })}
      </div>

      <p id="mobile-readonly" className="text-[12px] text-[var(--color-text-secondary)]">
        Human-in-the-loop: nothing is deleted until you confirm in the action bar.
      </p>
    </div>
  );
}
