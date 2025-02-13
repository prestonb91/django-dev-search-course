// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});

// Query selector that gets alert and then closes. 
let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

// When clicking the alert x button, then closes the alert. 
if (alertWrapper) {
  alertClose.addEventListener("click", () => (alertWrapper.style.display = "none"));
}