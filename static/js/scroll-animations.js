/* =============== Animatie la Scroll =============== */
document.addEventListener("DOMContentLoaded", function () {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate");
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  const elementsToAnimate = document.querySelectorAll(
    ".scroll-animate, .scroll-animate-left, .scroll-animate-right, .scroll-animate-scale",
  );

  elementsToAnimate.forEach((el) => observer.observe(el));
});
