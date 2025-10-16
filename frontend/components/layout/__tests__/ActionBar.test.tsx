import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ActionBar from "../ActionBar";

describe("ActionBar", () => {
  it("calls the keep best handler", async () => {
    const keep = vi.fn();
    const manual = vi.fn();
    const skip = vi.fn();

    const user = userEvent.setup();
    render(<ActionBar onKeepBest={keep} onManual={manual} onSkip={skip} />);

    await user.click(screen.getByRole("button", { name: /keep best/i }));
    expect(keep).toHaveBeenCalledTimes(1);
  });

  it("renders human-in-the-loop notice", () => {
    render(<ActionBar onKeepBest={() => undefined} onManual={() => undefined} onSkip={() => undefined} />);

    expect(screen.getByText(/No photos are deleted automatically/i)).toBeInTheDocument();
  });
});
