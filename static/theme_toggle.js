const toggleButton = document.getElementById('theme-toggle');
const themeLink = document.getElementById('theme-style');
  
toggleButton.addEventListener('click', () => {
    const currentTheme = themeLink.getAttribute('href').includes('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    themeLink.setAttribute('href', `/static/${newTheme}_theme.css`);
    localStorage.setItem('theme', newTheme);
});

// On page load, apply saved theme
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const themeLink = document.getElementById('theme-style');
    themeLink.setAttribute('href', `/static/${savedTheme}_theme.css`);  
});

window.addEventListener("scroll", () => {
    const button = document.getElementById("calculate-button");
    if (window.scrollY > 150) {
      button.classList.add("scrolled");
    } else {
      button.classList.remove("scrolled");
    }
  });