import type { Meta, StoryObj } from "@storybook/react";
import { Table, THead, TRow } from "./Table";

const meta: Meta<typeof Table> = {
  title: "UI/Table",
  component: Table
};

export default meta;

type Story = StoryObj<typeof Table>;

export const Overview: Story = {
  render: () => (
    <Table>
      <THead>
        <div className="grid grid-cols-3 gap-2 text-left">
          <span>Group</span>
          <span>Decision</span>
          <span>Date</span>
        </div>
      </THead>
      {[1, 2, 3].map((row) => (
        <TRow key={row}>
          <div className="grid grid-cols-3 gap-2 text-sm">
            <span>#20{row}</span>
            <span>Kept best photo</span>
            <span>13 Oct 2025</span>
          </div>
        </TRow>
      ))}
    </Table>
  )
};
