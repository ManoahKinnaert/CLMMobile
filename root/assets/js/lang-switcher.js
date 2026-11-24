document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("lang-btn");
  const content = document.getElementById("lang-content");
  const options = document.querySelectorAll(".lang-option");
  const toggle = document.querySelector(".nav-toggle");
  const links = document.getElementById("nav-links");

  const current = document.querySelector(".lang-option[aria-current='true']");
  if (current) btn.textContent = current.textContent;

  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-controls", "lang-content");

  const closeLang = () => {
    content.style.display = "none";
    btn.setAttribute("aria-expanded", "false");
  };

  const closeMenu = () => {
    if (links) links.classList.remove("open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  };

  btn.addEventListener("click", () => {
    const isOpen = content.style.display === "block";
    closeMenu();
    content.style.display = isOpen ? "none" : "block";
    btn.setAttribute("aria-expanded", String(!isOpen));
  });

  options.forEach((opt) => opt.addEventListener("click", closeLang));

  if (toggle && links) {
    toggle.setAttribute("aria-expanded", "false");

    toggle.addEventListener("click", () => {
      const isOpen = links.classList.contains("open");
      closeLang();
      links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(!isOpen));
    });

    links.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", closeMenu);
    });
  }

  document.addEventListener("click", (e) => {
    if (!e.target.closest("#lang-dropdown")) closeLang();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeLang();
      if (links && links.classList.contains("open")) {
        links.classList.remove("open");
        if (toggle) toggle.setAttribute("aria-expanded", "false");
      }
    }
  });
});
