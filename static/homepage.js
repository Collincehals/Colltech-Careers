window.addEventListener('scroll', function() {
  var button = document.querySelector('.back-to-top');
  if (window.pageYOffset > 200) { // Adjust the scroll position as needed
    button.style.display = 'block';
  } else {
    button.style.display = 'none';
  }
});
document.querySelector('.back-to-top').addEventListener('click', function(e) {
  e.preventDefault();
  window.scrollTo({ top: 0, behavior: 'smooth' });
});