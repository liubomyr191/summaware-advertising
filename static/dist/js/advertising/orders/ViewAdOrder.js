const navButtons = document.querySelectorAll('.button_nav');

const navLeft = document.querySelector('#nav_left');
const navRight = document.querySelector('#nav_right');

const orderDetailsPage = document.querySelector('#details_page');
const insertionsPage = document.querySelector('#insertions_page');
const historyPage = document.querySelector('#history_page');

const currentPageTitle = document.querySelector('#current_page');

const pageList = [];
navButtons.forEach(button => pageList.push(button.textContent));

let currentPage;
let currentTitle;

navButtons.forEach(button => {
    button.addEventListener('click', e => {
        navButtons.forEach(button => button.classList.remove('active'));
        e.target.classList.add('active');

        currentTitle = e.target.textContent;
        currentPageTitle.innerHTML = e.target.textContent;

        switch (e.target.id) {
            case 'order_details':
                orderDetailsPage.style.display = 'block';

                insertionsPage.style.display = 'none';
                historyPage.style.display = 'none';
                break;
            case 'insertions':
                insertionsPage.style.display = 'flex';

                orderDetailsPage.style.display = 'none';
                historyPage.style.display = 'none';
                break;
            case 'history_logs':
                historyPage.style.display = 'block';

                orderDetailsPage.style.display = 'none';
                insertionsPage.style.display = 'none';
                break;
        }
    });
});

let currentIndex = 0;
navLeft.addEventListener('click', e => {

});

$(document).ready(function (e) {
    orderDetailsPage.style.display = 'block';
    insertionsPage.style.display = 'none';
    historyPage.style.display = 'none';
})