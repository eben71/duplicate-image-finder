import type { Meta, StoryObj } from "@storybook/react";
import Button from "./Button";

const meta: Meta<typeof Button> = {
  title: "UI/Button",
  component: Button,
  parameters: { layout: "centered" }
};

export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: "Primary button"
  }
};

export const Secondary: Story = {
  args: {
    variant: "secondary",
    children: "Secondary"
  }
};

export const Ghost: Story = {
  args: {
    variant: "ghost",
    children: "Ghost"
  }
};
