// funzioni
function goBack() {
    window.history.back();
}
// elementi presi dall'html
const themeToggleBtn = document.querySelector('.theme-toggle');
const lightIcon = document.getElementById('lightIcon');
const darkIcon = document.getElementById('darkIcon');
// tema dal local storage
const theme = localStorage.getItem('theme');

// logica appena attivato lo script
if (theme) {
    document.body.classList.add(theme);
    darkIcon.classList.add('hidden');
}
else {
    lightIcon.classList.add('hidden');
}

// azione del bottone
themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');

    if (document.body.classList.contains('light-mode')) {
        localStorage.setItem('theme', 'light-mode');
        darkIcon.classList.add('hidden');
        lightIcon.classList.remove('hidden');
    } else {
        localStorage.removeItem('theme');
        lightIcon.classList.add('hidden');
        darkIcon.classList.remove('hidden');
    }
});