// script star rating 
document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll(".star");
  const ratingInput = document.getElementById('ratingInput');

  stars.forEach(function(star) {
      star.addEventListener("mouseover", function() {
          const rating = parseInt(star.getAttribute("data-rating"));
          selectStars(rating);
      });
  });

  function selectStars(rating) {
      ratingInput.value = rating;
      stars.forEach(function(star) {
        const starRating = parseInt(star.getAttribute("data-rating"));
        
          star.style.color = (starRating <= rating) ? "red" : "black";
      });
  }
});

// script bouton plus 

document.addEventListener("DOMContentLoaded", function() {
  const loadMoreBtn = document.getElementById("loadMoreBtn");
  const ticketsAndReviewsContainer = document.getElementById("ticketsAndReviewsContainer");

  let page = 1;

  loadMoreBtn.addEventListener("click", function() {
    page++;
    const url = `?page=${page}`;
    fetch(url)
      .then(response => response.text())
      .then(data => {
        const parser = new DOMParser();
        const htmlDocument = parser.parseFromString(data, "text/html");
        const newItems = htmlDocument.getElementById("ticketsAndReviewsContainer").innerHTML;
        ticketsAndReviewsContainer.innerHTML += newItems;
        if (!htmlDocument.getElementById("loadMoreBtn")) {
          loadMoreBtn.style.display = "none";
        }
      })
      .catch(error => console.error("Error fetching data:", error));
  });
});