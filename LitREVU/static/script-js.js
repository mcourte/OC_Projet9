document.addEventListener("DOMContentLoaded", function() {
    // Ajouter un effet au survol des champs d'entrée
    function addInputHoverEffect() {
        const inputs = document.querySelectorAll('input');
        inputs.forEach(function(input) {
            input.addEventListener('mouseenter', function() {
                this.classList.add('input-hover');
            });
            input.addEventListener('mouseleave', function() {
                this.classList.remove('input-hover');
            });
        });
    }

    // Récupérer la valeur du cookie CSRF
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

    // Vérifie si l'utilisateur utilise un lecteur d'écran
    function isScreenReaderActive() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    // Gérer la sélection de la note en cliquant sur les étoiles dans le formulaire de critique
    function setupRatingStars() {
        const stars = document.querySelectorAll(".star");
        const ratingInput = document.getElementById('rating');
        stars.forEach(function(star) {
            star.addEventListener("click", function() {
                const rating = parseInt(star.getAttribute("data-rating"));
                ratingInput.value = rating;
                stars.forEach(function(s) {
                    const sRating = parseInt(s.getAttribute("data-rating"));
                    s.style.color = sRating <= rating ? "gold" : "black";
                });
            });
        });
    }

    // Gérer le clic sur le bouton de suppression de ticket
    function setupDeleteButtons() {
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

        // Gérer le clic sur le bouton de suppression de critique
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
                            window.location.reload();
                        } else {
                            console.error('Erreur lors de la suppression de la critique');
                        }
                    })
                    .catch(error => {
                        console.error('Erreur lors de la suppression de la critique :', error);
                    });
                }
            });
        });
    }
})


// Fonction pour afficher une page de tickets et de critiques
document.addEventListener("DOMContentLoaded", function() {
    function setupPagination() {
        const tickets = document.querySelectorAll('.ticket');
        const itemsPerPage = 4;
        let currentPage = 1;

        function showPage(page) {
            const startIndex = (page - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;

            tickets.forEach((ticket, index) => {
                ticket.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
            });

            const totalPages = Math.ceil(tickets.length / itemsPerPage);
            const prevButton = document.getElementById('prevPage');
            const nextButton = document.getElementById('nextPage');

            prevButton.style.display = (page === 1) ? 'none' : 'inline-block';
            nextButton.style.display = (page === totalPages) ? 'none' : 'inline-block';
        }

        document.getElementById('prevPage').addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                showPage(currentPage);
            }
        });

        document.getElementById('nextPage').addEventListener('click', function() {
            const totalPages = Math.ceil(tickets.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                showPage(currentPage);
            }
        });

        showPage(currentPage);
    }

    setupPagination();
});
