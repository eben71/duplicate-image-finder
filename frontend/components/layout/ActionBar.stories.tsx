import type { Meta, StoryObj } from "@storybook/react";
import ActionBar from "./ActionBar";

const meta: Meta<typeof ActionBar> = {
  title: "Layout/ActionBar",
  component: ActionBar
};

export default meta;

type Story = StoryObj<typeof ActionBar>;

export const Default: Story = {
  args: {
    onKeepBest: () => undefined,
    onManual: () => undefined,
    onSkip: () => undefined
  }
};
