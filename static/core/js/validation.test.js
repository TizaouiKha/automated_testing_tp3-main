const { isFilled, isValidEmail, isValidPhoneNumber, isFieldValid, getErrorMessage } = require("./validation");

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

describe("isFieldValid", () => {
  test("returns true for a valid email field", () => {
    expect(isFieldValid({ type: "email", value: "alice@example.com", dataset: {} })).toBe(true);
  });

  test("returns false for an invalid email field", () => {
    expect(isFieldValid({ type: "email", value: "bob", dataset: {} })).toBe(false);
  });

  test("returns true for a valid phone_number field", () => {
    expect(isFieldValid({ type: "text", value: "+33 06-12-34-56-78", dataset: { type: "phone_number", required: "true" } })).toBe(true);
  });

  test("returns false for an invalid phone_number field", () => {
    expect(isFieldValid({ type: "text", value: "abc", dataset: { type: "phone_number", required: "true" } })).toBe(false);
  });

  test("returns true for a filled required field", () => {
    expect(isFieldValid({ type: "text", value: "Alice", dataset: { required: "true" } })).toBe(true);
  });

  test("returns false for an empty required field", () => {
    expect(isFieldValid({ type: "text", value: "", dataset: { required: "true" } })).toBe(false);
  });

  test("returns true for an optional empty field", () => {
    expect(isFieldValid({ type: "text", value: "", dataset: {} })).toBe(true);
  });
});

describe("getErrorMessage", () => {
  test("returns 'Invalid email address' for invalid email", () => {
    expect(getErrorMessage({ type: "email", value: "bob", dataset: {} })).toBe("Invalid email address");
  });

  test("returns null for valid email", () => {
    expect(getErrorMessage({ type: "email", value: "alice@example.com", dataset: {} })).toBeNull();
  });

  test("returns 'Invalid phone number' for invalid phone", () => {
    expect(getErrorMessage({ type: "text", value: "abc", dataset: { type: "phone_number" } })).toBe("Invalid phone number");
  });

  test("returns null for valid phone", () => {
    expect(getErrorMessage({ type: "text", value: "06-12-34-56-78", dataset: { type: "phone_number" } })).toBeNull();
  });

  test("returns 'Mandatory field' for empty required field", () => {
    expect(getErrorMessage({ type: "text", value: "", dataset: { required: "true" } })).toBe("Mandatory field");
  });

  test("returns null for filled required field", () => {
    expect(getErrorMessage({ type: "text", value: "Alice", dataset: { required: "true" } })).toBeNull();
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
