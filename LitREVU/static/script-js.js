

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

    // Fonction pour gérer le clic sur le bouton de suppression de ticket
    document.querySelectorAll('.delete-ticket-button').forEach(button => {
      button.addEventListener('click', function(event) {
          event.preventDefault();
          const ticketId = this.dataset.ticketId;
          const confirmation = confirm("Êtes-vous sûr de vouloir supprimer ce ticket ?");
          if (confirmation) {
              document.getElementById('delete_ticket_form_' + ticketId).submit();
          }
      });
  });

  // Fonction pour gérer le clic sur le bouton de suppression de critique
  document.querySelectorAll('.delete-review-button').forEach(button => {
      button.addEventListener('click', function(event) {
          event.preventDefault();
          const reviewId = this.dataset.reviewId;
          const confirmation = confirm("Êtes-vous sûr de vouloir supprimer cette critique ?");
          if (confirmation) {
              document.getElementById('delete_review_form_' + reviewId).submit();
          }
      });
  });