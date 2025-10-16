import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import Modal from "./Modal";
import Button from "./Button";

const meta: Meta<typeof Modal> = {
  title: "UI/Modal",
  component: Modal,
  parameters: { layout: "centered" }
};

export default meta;

type Story = StoryObj<typeof Modal>;

export const Basic: Story = {
  render: function Render() {
    const [open, setOpen] = useState(true);
    return (
      <div className="space-y-4">
        <Button onClick={() => setOpen(true)}>Open dialog</Button>
        <Modal
          open={open}
          title="Confirm delete"
          description="Photos are moved to Google Photos Trash when you confirm."
          onClose={() => setOpen(false)}
          actions={
            <>
              <Button variant="ghost" onClick={() => setOpen(false)}>
                Cancel
              </Button>
              <Button onClick={() => setOpen(false)}>Keep best + delete others</Button>
            </>
          }
        >
          <p className="text-sm text-[var(--color-text-secondary)]">
            Human-in-the-loop confirmation required before anything is removed.
          </p>
        </Modal>
      </div>
    );
  }
};
