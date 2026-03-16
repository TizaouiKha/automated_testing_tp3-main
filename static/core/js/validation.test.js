const { isFilled } = require("./validation");

describe("isFilled", () => {
  test("returns false for an empty string", () => {
    expect(isFilled("")).toBe(false);
  });

  test("returns true for a non-empty string", () => {
    expect(isFilled("Something!")).toBe(true);
  });

  test("returns false for a whitespace-only string", () => {
    expect(isFilled("   ")).toBe(false);
  });
});
