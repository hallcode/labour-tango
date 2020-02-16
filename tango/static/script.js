function togglePageMenu() {
    let pageMenu = document.querySelector('#pageMenu');
    let icon     = document.querySelector('#pageMenuIcon');

    pageMenu.classList.toggle('open');
    icon.classList.toggle('icon-menu');
    icon.classList.toggle('icon-cross');
}

function toggleMainMenu() {
    let menu = document.querySelector('#mainMenu');
    let icon     = document.querySelector('#mainMenuIcon');

    menu.classList.toggle('open');
    icon.classList.toggle('icon-apps');
    icon.classList.toggle('icon-cross');
}