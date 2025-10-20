import { render, screen, fireEvent } from "@testing-library/react";
import ComparePanel from "../ComparePanel";

describe("ComparePanel", () => {
  beforeEach(() => {
    window.innerWidth = 1280;
  });

  it("renders layout toggle buttons", () => {
    render(<ComparePanel />);

    expect(screen.getByRole("radio", { name: "2-up" })).toHaveAttribute("aria-checked", "true");
    expect(screen.getByRole("radio", { name: "4-up" })).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: "8-up" })).toBeInTheDocument();
  });

  it("announces the selected comparison layout when toggled", () => {
    render(<ComparePanel />);

    const fourUp = screen.getByRole("radio", { name: "4-up" });
    fireEvent.click(fourUp);

    expect(fourUp).toHaveAttribute("aria-checked", "true");
    expect(screen.getByLabelText(/showing 4-up comparison/i)).toBeInTheDocument();
  });

  it("disables interactions on mobile widths", async () => {
    window.innerWidth = 375;
    render(<ComparePanel />);

    const checkbox = await screen.findAllByRole("checkbox");
    expect(checkbox[0]).toBeDisabled();
    expect(await screen.findByText(/desktop-only/i)).toBeInTheDocument();
  });
});
