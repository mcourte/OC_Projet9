document.querySelectorAll('input').forEach(input => {
    input.addEventListener('mouseover', () => {
      input.nextElementSibling.style.display = 'block';
    });
  
    input.addEventListener('mouseout', () => {
      input.nextElementSibling.style.display = 'none';
    });
  });