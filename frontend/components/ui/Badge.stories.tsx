import type { Meta, StoryObj } from "@storybook/react";
import Badge from "./Badge";

const meta: Meta<typeof Badge> = {
  title: "UI/Badge",
  component: Badge,
  args: { children: "Keep" }
};

export default meta;

type Story = StoryObj<typeof Badge>;

export const Keep: Story = {
  args: { type: "keep" }
};

export const Unsure: Story = {
  args: { type: "unsure", children: "Unsure" }
};

export const Low: Story = {
  args: { type: "low", children: "Low confidence" }
};
