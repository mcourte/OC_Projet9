// input-hover.js

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Get all input fields
  var inputs = document.querySelectorAll('input');

  // Loop through each input field
  inputs.forEach(function(input) {
      // Add event listeners for mouse enter and mouse leave
      input.addEventListener('mouseenter', function() {
          // Add a class to highlight the input field on hover
          this.classList.add('input-hover');
      });
      input.addEventListener('mouseleave', function() {
          // Remove the class when the mouse leaves the input field
          this.classList.remove('input-hover');
      });
  });
});