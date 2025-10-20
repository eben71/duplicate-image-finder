import type { Meta, StoryObj } from "@storybook/react";
import ComparePanel from "./ComparePanel";

const meta: Meta<typeof ComparePanel> = {
  title: "Review/ComparePanel",
  component: ComparePanel
};

export default meta;

type Story = StoryObj<typeof ComparePanel>;

export const Default: Story = {
  render: () => <ComparePanel />
};
