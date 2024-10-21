// html elements
const themeToggleBtn = document.querySelector('.theme-toggle');
const lightIcon = document.getElementById('lightIcon');
const darkIcon = document.getElementById('darkIcon');

// get current theme
const theme = localStorage.getItem('theme');

// adding classes to the body and icons based on current theme
if (theme) {
    document.body.classList.add(theme);
    darkIcon.classList.add('hidden');
}
else {
    lightIcon.classList.add('hidden');
}

// toggle between icons and add to local storace current theme mode
themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');

    if (document.body.classList.contains('light-mode')) {
        localStorage.setItem('theme', 'light-mode');
        darkIcon.classList.add('hidden');
        lightIcon.classList.remove('hidden');
        lightIcon.classList.add('fade-in');

    } else {
        localStorage.removeItem('theme');
        lightIcon.classList.add('hidden');
        darkIcon.classList.remove('hidden');
        darkIcon.classList.add('fade-in');
    }

    // timeout that removes animation after it's finished
    setTimeout(() => {
        lightIcon.classList.remove('fade-in');
        darkIcon.classList.remove('fade-in');
    }, 500);

});