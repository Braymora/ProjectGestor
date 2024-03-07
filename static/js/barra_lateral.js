const toggle = document.querySelector(".toggle");
const menuDashboard = document.querySelector(".menu-dashboard");
const iconoMenu = toggle.querySelector("i");
const enlacesMenu = document.querySelectorAll(".enlace");

// Activar el menú al dar clic
toggle.addEventListener("click", () => {
  menuDashboard.classList.toggle("open");
  iconoMenu.classList.toggle("rotated"); // Añade o remueve la clase rotated al icono
});

// Manejar clics en los enlaces del menú
enlacesMenu.forEach(enlace => {
  enlace.addEventListener("click", () => {
    menuDashboard.classList.add("open");
    iconoMenu.classList.replace("bx-menu", "bx-x");
    iconoMenu.classList.add("rotated"); // Asegúrate de que el icono esté rotado cuando se haga clic en un enlace
  });
});
