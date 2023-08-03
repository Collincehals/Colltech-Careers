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


var swiper = new Swiper(".review-swiper", {
      spaceBetween: 30,
      centeredSlides: true,
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      loop: true,
      breakpoints: {
        0:{
          slidesPerView: 1,
        },
         640:{
          slidesPerView: 2,
        },
         768:{
          slidesPerView: 2,
        },
         1025:{
          slidesPerView: 3,
        },
      },
    });