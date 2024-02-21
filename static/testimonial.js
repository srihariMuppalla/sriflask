let slideIndex = 0;
const testimonials = document.querySelectorAll('.carousel li');
const intervalTime = 5000; // Change slide every 5 seconds

function autoSlide() {
  nextTestimonial();
  setTimeout(autoSlide, intervalTime);
}

autoSlide();

function prevTestimonial() {
  slideIndex--;
  if (slideIndex < 0) {
    slideIndex = testimonials.length - 1;
  }
  updateSlide();
}

function nextTestimonial() {
  slideIndex++;
  if (slideIndex >= testimonials.length) {
    slideIndex = 0;
  }
  updateSlide();
}

function updateSlide() {
  testimonials.forEach(testimonial => testimonial.style.display = 'none');
  testimonials[slideIndex].style.display = 'flex';
}