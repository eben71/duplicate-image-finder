"use client";
import React from "react";
interface ModalProps {
  open: boolean;
  title: string;
  description?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  onClose?: () => void;
}
export default function Modal({ open, title, description, children, actions, onClose }: ModalProps) {
  if (!open) return null;
  return (
    <div
      aria-modal
      role="presentation"
      className="fixed inset-0 z-50 grid place-items-center bg-black/45 px-4"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-labelledby="modal-title"
        aria-describedby={description ? "modal-description" : undefined}
        className="w-[640px] max-w-full rounded-[var(--radius-lg)] bg-white p-[var(--space-xl)] shadow-[0_8px_16px_var(--color-shadow-high)]"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 id="modal-title" className="text-[22px] font-semibold mb-[var(--space-sm)]">{title}</h2>
            {description && (
              <p id="modal-description" className="text-[14px] text-[var(--color-text-secondary)]">
                {description}
              </p>
            )}
          </div>
          {onClose && (
            <button onClick={onClose} aria-label="Close dialog" className="focus-ring text-[var(--color-text-secondary)]">
              ✕
            </button>
          )}
        </div>
        <div className="mt-[var(--space-md)]">{children}</div>
        {actions && <div className="mt-[var(--space-xl)] flex flex-wrap gap-[var(--space-md)] justify-end">{actions}</div>}
      </div>
    </div>
  );
}
