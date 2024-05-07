// Fonction pour ajouter un effet au survol des champs d'entrée
function addInputHoverEffect() {
  // Obtenir tous les champs d'entrée
  var inputs = document.querySelectorAll('input');

  // Parcourir chaque champ d'entrée
  inputs.forEach(function(input) {
      // Ajouter des écouteurs d'événements pour la souris entrante et sortante
      input.addEventListener('mouseenter', function() {
          // Ajouter une classe pour mettre en surbrillance le champ d'entrée au survol
          this.classList.add('input-hover');
      });
      input.addEventListener('mouseleave', function() {
          // Supprimer la classe lorsque la souris quitte le champ d'entrée
          this.classList.remove('input-hover');
      });
  });
}

// JavaScript pour la sélection de la note en cliquant sur les étoiles
document.addEventListener("DOMContentLoaded", function() {
  const stars = document.querySelectorAll(".star");
  const ratingInput = document.getElementById('rating');

  stars.forEach(function(star) {
      star.addEventListener("click", function() {
          const rating = parseInt(star.getAttribute("data-rating"));
          ratingInput.value = rating;

          // Mettre à jour la couleur des étoiles en fonction de la note sélectionnée
          stars.forEach(function(s) {
              const sRating = parseInt(s.getAttribute("data-rating"));
              s.style.color = sRating <= rating ? "gold" : "black";
          });
      });
  });

  // Appeler la fonction pour ajouter l'effet au survol des champs d'entrée
  addInputHoverEffect();

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
              fetch(`/review/edit_delete_review/${reviewId}/`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: JSON.stringify({ reviewId: reviewId })
              })
              .then(response => {
                  if (response.ok) {
                      // Rediriger ou effectuer toute autre action après suppression réussie
                      window.location.reload(); // Exemple : recharger la page
                  } else {
                      // Gérer les erreurs ou afficher un message à l'utilisateur
                      console.error('Erreur lors de la suppression de la critique');
                  }
              })
              .catch(error => {
                  console.error('Erreur lors de la suppression de la critique :', error);
              });
          }
      });
  });

  // Fonction pour récupérer la valeur du cookie CSRF
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  // Fonction pour gérer la sélection de la note en cliquant sur les étoiles dans le formulaire de critique
  const ratingStars = document.querySelectorAll(".rating .star");

  ratingStars.forEach(function(star) {
      star.addEventListener("click", function() {
          const rating = this.getAttribute("data-rating");
          // Mettez à jour la valeur du champ de notation caché
          document.getElementById("rating").value = rating;
          // Mettre en surbrillance les étoiles sélectionnées et changer leur couleur
          ratingStars.forEach(function(s) {
              if (s.getAttribute("data-rating") <= rating) {
                  s.classList.add("selected");
                  s.style.color = "gold"; // Changez la couleur des étoiles sélectionnées ici
              } else {
                  s.classList.remove("selected");
                  s.style.color = "black"; // Changez la couleur des étoiles non sélectionnées ici
              }
          });
      });
  });

  // Fonction pour afficher une page de tickets et de critiques
  const tickets = document.querySelectorAll('.ticket');
  const reviews = document.querySelectorAll('.review');
  const itemsPerPage = 2;
  let currentPage = 1;

  function showPage(page) {
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;

      tickets.forEach((ticket, index) => {
          ticket.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
      });

      reviews.forEach((review, index) => {
          review.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
      });

      const totalPages = Math.ceil(Math.max(tickets.length, reviews.length) / itemsPerPage);
      const prevButton = document.getElementById('prevPage');
      const nextButton = document.getElementById('nextPage');

      if (currentPage === 1) {
          prevButton.style.display = 'none';
      } else {
          prevButton.style.display = 'block';
      }

      if (currentPage === totalPages) {
          nextButton.style.display = 'none';
      } else {
          nextButton.style.display = 'block';
      }
  }

  document.getElementById('prevPage').addEventListener('click', function() {
      if (currentPage > 1) {
          currentPage--;
          showPage(currentPage);
      }
  });

  document.getElementById('nextPage').addEventListener('click', function() {
      const totalPages = Math.ceil(Math.max(tickets.length, reviews.length) / itemsPerPage);
      if (currentPage < totalPages) {
          currentPage++;
          showPage(currentPage);
      }
  });

  showPage(currentPage);
});
