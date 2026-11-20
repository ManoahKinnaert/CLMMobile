document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("lang-btn");
  const content = document.getElementById("lang-content");
  const options = document.querySelectorAll(".lang-option");

  const current = document.querySelector(".lang-option[aria-current='true']");
  if (current) btn.textContent = current.textContent;

  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-controls", "lang-content");

  const close = () => {
    content.style.display = "none";
    btn.setAttribute("aria-expanded", "false");
  };

  btn.addEventListener("click", () => {
    const isOpen = content.style.display === "block";
    content.style.display = isOpen ? "none" : "block";
    btn.setAttribute("aria-expanded", String(!isOpen));
  });

  options.forEach((opt) => opt.addEventListener("click", close));

  document.addEventListener("click", (e) => {
    if (!e.target.closest("#lang-dropdown")) close();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
});
