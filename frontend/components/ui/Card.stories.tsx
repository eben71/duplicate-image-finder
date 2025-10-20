import type { Meta, StoryObj } from "@storybook/react";
import Card from "./Card";

const meta: Meta<typeof Card> = {
  title: "UI/Card",
  component: Card,
  parameters: { layout: "centered" }
};

export default meta;

type Story = StoryObj<typeof Card>;

export const Default: Story = {
  render: () => (
    <Card>
      <h3 className="text-lg font-semibold">Card heading</h3>
      <p className="text-sm text-[var(--color-text-secondary)]">Token-driven surface with default padding.</p>
    </Card>
  )
};
