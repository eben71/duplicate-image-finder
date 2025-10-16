interface FilmstripItem {
  id: string;
  thumbnail: string;
  alt: string;
  isPrimary?: boolean;
}

interface FilmstripProps {
  items: FilmstripItem[];
  onSelect: (id: string) => void;
  activeId: string;
}

export default function Filmstrip({ items, onSelect, activeId }: FilmstripProps) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-2" aria-label="Group thumbnails">
      {items.map((item) => {
        const active = item.id === activeId;
        return (
          <button
            key={item.id}
            onClick={() => onSelect(item.id)}
            className={`focus-ring relative h-20 w-20 flex-shrink-0 overflow-hidden rounded-[var(--radius-sm)] border ${active ? "border-[var(--color-primary-base)]" : "border-[var(--color-ui-border)]"}`}
            aria-pressed={active}
            aria-label={item.alt}
          >
            <span
              className="block h-full w-full"
              aria-hidden
              style={{ backgroundImage: item.thumbnail, backgroundSize: "cover", backgroundPosition: "center" }}
            />
            <span className="sr-only">{item.alt}</span>
            {item.isPrimary && (
              <span className="absolute bottom-1 left-1 rounded bg-black/60 px-1 text-[10px] text-white">AI KEEP</span>
            )}
          </button>
        );
      })}
    </div>
  );
}
