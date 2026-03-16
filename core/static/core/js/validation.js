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
 * Wire up blur/input validation for all required fields on the page.
 * Called once the DOM is ready.
 */
function initRequiredFieldValidation() {
  document.querySelectorAll('[data-required="true"]').forEach(function (field) {
    field.addEventListener("blur", function () {
      var errorId = "error_" + field.id.split("_")[1];
      var errorSpan = document.getElementById(errorId);

      if (!isFilled(field.value)) {
        field.classList.add("field-error");
        if (errorSpan) errorSpan.classList.add("visible");
      } else {
        field.classList.remove("field-error");
        if (errorSpan) errorSpan.classList.remove("visible");
      }
    });

    field.addEventListener("input", function () {
      if (isFilled(field.value)) {
        var errorId = "error_" + field.id.split("_")[1];
        var errorSpan = document.getElementById(errorId);
        field.classList.remove("field-error");
        if (errorSpan) errorSpan.classList.remove("visible");
      }
    });
  });
}


// Allow both browser usage and Node.js/Jest imports
if (typeof module !== "undefined" && module.exports) {
  module.exports = { isFilled };
}
