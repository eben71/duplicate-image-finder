import type { Meta, StoryObj } from "@storybook/react";
import GroupCard from "./GroupCard";

const meta: Meta<typeof GroupCard> = {
  title: "Review/GroupCard",
  component: GroupCard,
  args: {
    id: "203",
    count: 6,
    range: "94–98%",
    badge: { type: "keep", text: "KEEP 94%" }
  }
};

export default meta;

type Story = StoryObj<typeof GroupCard>;

export const Default: Story = {
  args: {
    onOpen: () => undefined
  }
};

export const Unsure: Story = {
  args: {
    id: "204",
    badge: { type: "unsure", text: "UNSURE 85%" },
    onOpen: () => undefined
  }
};
