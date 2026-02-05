/* =============== SCROLL UP =============== */
const scrollUp = () => {
  const scrollUpBtn = document.getElementById("scroll-up");
  if (scrollUpBtn) {
    window.scrollY >= 350
      ? scrollUpBtn.classList.add("show-scroll")
      : scrollUpBtn.classList.remove("show-scroll");
  }
};
window.addEventListener("scroll", scrollUp);
