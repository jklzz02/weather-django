const themeToggleBtn = document.querySelector('.theme-toggle');
const theme = localStorage.getItem('theme');


if (theme) {
    document.body.classList.add(theme);
}

themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');

    if (document.body.classList.contains('light-mode')) {
        localStorage.setItem('theme', 'light-mode');
    } else {
        localStorage.removeItem('theme');
    }
});