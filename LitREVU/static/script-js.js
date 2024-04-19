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


  document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const ratingInput = document.getElementById('rating');
  
    stars.forEach(function(star) {
      star.addEventListener("click", function() {
        const rating = parseInt(star.getAttribute("data-rating"));
        ratingInput.value = rating;
  
        // Mettre à jour la couleur des étoiles en fonction de la note sélectionnée
        stars.forEach(function(s) {
          const sRating = parseInt(s.getAttribute("data-rating"));
          s.style.color = sRating <= rating ? "yellow" : "black";
        });
      });
    });
  });