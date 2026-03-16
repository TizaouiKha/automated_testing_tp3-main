/**
 * Returns true if text is not empty (after trimming whitespace).
 *
 * @param {string} text
 * @returns {boolean}
 */
function isFilled(text) {
  return text.trim() !== "";
}


/**
 * Returns true if text is a valid phone number.
 * Allows digits, spaces and dashes.
 * Optionally starts with + followed by exactly 2 digits.
 *
 * @param {string} text
 * @returns {boolean}
 */
function isValidPhoneNumber(text) {
  return /^(\+\d{2})?[\d\s\-]+$/.test(text) && text.trim().length > 0;
}


/**
 * Returns null if the field is valid, or an error message string if not.
 *
 * @param {HTMLElement} field
 * @returns {string|null}
 */
function getErrorMessage(field) {
  if (field.type === "email") {
    if (!isValidEmail(field.value)) return "Invalid email address";
  } else if (field.dataset.type === "phone_number") {
    if (!isValidPhoneNumber(field.value)) return "Invalid phone number";
  } else if (field.dataset.required === "true") {
    if (!isFilled(field.value)) return "Mandatory field";
  }
  return null;
}


/**
 * Wire up blur/input validation for all required fields on the page.
 * Called once the DOM is ready.
 */
function initRequiredFieldValidation() {
  document.querySelectorAll('[data-required="true"]').forEach(function (field) {
    field.addEventListener("blur", function () {
      var errorId = "error_" + field.id.split("_")[1];
      var errorSpan = document.getElementById(errorId);
      var errorMsg = getErrorMessage(field);

      if (errorMsg) {
        field.classList.add("field-error");
        if (errorSpan) {
          errorSpan.textContent = errorMsg;
          errorSpan.classList.add("visible");
        }
      } else {
        field.classList.remove("field-error");
        if (errorSpan) errorSpan.classList.remove("visible");
      }
    });

    field.addEventListener("input", function () {
      var errorId = "error_" + field.id.split("_")[1];
      var errorSpan = document.getElementById(errorId);
      if (!getErrorMessage(field)) {
        field.classList.remove("field-error");
        if (errorSpan) errorSpan.classList.remove("visible");
      }
    });
  });
}


/**
 * Returns true if text is a valid email address.
 *
 * @param {string} text
 * @returns {boolean}
 */
function isValidEmail(text) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text);
}


// Allow both browser usage and Node.js/Jest imports
if (typeof module !== "undefined" && module.exports) {
  module.exports = { isFilled, isValidEmail, isValidPhoneNumber };
}
