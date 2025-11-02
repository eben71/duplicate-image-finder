import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import Filmstrip from "./Filmstrip";

const items = [
  { id: "1", thumbnail: "linear-gradient(135deg, #2F80ED 0%, #56CCF2 100%)", alt: "Option 1", isPrimary: true },
  { id: "2", thumbnail: "linear-gradient(135deg, #F2994A 0%, #F2C94C 100%)", alt: "Option 2" },
  { id: "3", thumbnail: "linear-gradient(135deg, #27AE60 0%, #6FCF97 100%)", alt: "Option 3" }
];

const meta: Meta<typeof Filmstrip> = {
  title: "Review/Filmstrip",
  component: Filmstrip
};

export default meta;

type Story = StoryObj<typeof Filmstrip>;

export const Default: Story = {
  render: function Render() {
    const [active, setActive] = useState(items[0]?.id ?? "");
    return <Filmstrip items={items} onSelect={setActive} activeId={active} />;
  }
};
