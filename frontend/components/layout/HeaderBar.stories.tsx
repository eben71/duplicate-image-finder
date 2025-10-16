import type { Meta, StoryObj } from "@storybook/react";
import HeaderBar from "./HeaderBar";

const meta: Meta<typeof HeaderBar> = {
  title: "Layout/HeaderBar",
  component: HeaderBar
};

export default meta;

type Story = StoryObj<typeof HeaderBar>;

export const Default: Story = {
  render: () => <HeaderBar />
};
