const { isFilled, isValidEmail, isValidPhoneNumber } = require("./validation");

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

describe("isValidEmail", () => {
  test("returns true for a valid email", () => {
    expect(isValidEmail("alice@example.com")).toBe(true);
  });

  test("returns false for missing @", () => {
    expect(isValidEmail("bob")).toBe(false);
  });

  test("returns false for missing domain", () => {
    expect(isValidEmail("bob@")).toBe(false);
  });

  test("returns false for missing local part", () => {
    expect(isValidEmail("@example.com")).toBe(false);
  });

  test("returns false for empty string", () => {
    expect(isValidEmail("")).toBe(false);
  });

  test("returns true for email with subdomain", () => {
    expect(isValidEmail("user@mail.example.com")).toBe(true);
  });
});

describe("isValidPhoneNumber", () => {
  test("returns true for digits only", () => {
    expect(isValidPhoneNumber("0612345678")).toBe(true);
  });

  test("returns true with spaces and dashes", () => {
    expect(isValidPhoneNumber("06-12 34 56 78")).toBe(true);
  });

  test("returns true with + prefix and 2 digits country code", () => {
    expect(isValidPhoneNumber("+33 06-12-34-56-78")).toBe(true);
  });

  test("returns false for letters", () => {
    expect(isValidPhoneNumber("abc-def")).toBe(false);
  });

  test("returns false for + not in first position", () => {
    expect(isValidPhoneNumber("06+12345678")).toBe(false);
  });

  test("returns false for + without 2 digits after", () => {
    expect(isValidPhoneNumber("+3 06")).toBe(false);
  });

  test("returns false for empty string", () => {
    expect(isValidPhoneNumber("")).toBe(false);
  });
});
