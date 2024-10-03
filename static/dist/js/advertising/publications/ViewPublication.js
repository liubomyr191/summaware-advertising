const navigateBtns = document.querySelectorAll('.page_nav');
const headerNavigateBtns = document.querySelectorAll('.button_nav');

const detailsPage = document.querySelector('#details_page');
const deadlinesPage = document.querySelector('#ad_deadlines_page');
const dimensionsPage = document.querySelector('#page_dimensions_page');
const adjustmentsPage = document.querySelector('#adjustments_page');
const defaultStylesPage = document.querySelector('#default_styles_page');
const financePage = document.querySelector('#finance_page');
const sectionsPage = document.querySelector('#sections_page');

const currentPageTitle = document.querySelector('#current_page');

$(document).ready(function () {
    detailsPage.style.display = 'block';
});

headerNavigateBtns.forEach(button => {
    button.addEventListener('click', e => {
        headerNavigateBtns.forEach(button => button.classList.remove('active'));
        e.target.classList.add('active');

        currentTitle = e.target.textContent;
        currentPageTitle.innerHTML = e.target.textContent;

        switch (e.target.id) {
            case 'details':
                detailsPage.style.display = 'block';
                deadlinesPage.style.display = 'none';
                dimensionsPage.style.display = 'none';
                adjustmentsPage.style.display = 'none';
                defaultStylesPage.style.display = 'none';
                financePage.style.display = 'none';
                sectionsPage.style.display = 'none';
                break;
            case 'ad_deadlines':
                detailsPage.style.display = 'none';
                deadlinesPage.style.display = 'block';

                dimensionsPage.style.display = 'none';
                adjustmentsPage.style.display = 'none';
                defaultStylesPage.style.display = 'none';
                financePage.style.display = 'none';
                sectionsPage.style.display = 'none';
                break;
            case 'page_dimensions':
                detailsPage.style.display = 'none';
                deadlinesPage.style.display = 'none';
                dimensionsPage.style.display = 'block';
                adjustmentsPage.style.display = 'none';
                defaultStylesPage.style.display = 'none';
                financePage.style.display = 'none';
                sectionsPage.style.display = 'none';
                break;
            case 'adjustments':
                detailsPage.style.display = 'none';
                deadlinesPage.style.display = 'none';
                dimensionsPage.style.display = 'none';
                adjustmentsPage.style.display = 'block';
                defaultStylesPage.style.display = 'none';
                financePage.style.display = 'none';
                sectionsPage.style.display = 'none';
                break;
            case 'default_styles':
                detailsPage.style.display = 'none';
                deadlinesPage.style.display = 'none';
                dimensionsPage.style.display = 'none';
                adjustmentsPage.style.display = 'none';
                defaultStylesPage.style.display = 'block';
                financePage.style.display = 'none';
                sectionsPage.style.display = 'none';
                break;
            case 'finance':
                detailsPage.style.display = 'none';
                deadlinesPage.style.display = 'none';
                dimensionsPage.style.display = 'none';
                adjustmentsPage.style.display = 'none';
                defaultStylesPage.style.display = 'none';
                financePage.style.display = 'block';
                sectionsPage.style.display = 'none';
                break;
            case 'sections':
                detailsPage.style.display = 'none';
                deadlinesPage.style.display = 'none';
                dimensionsPage.style.display = 'none';
                adjustmentsPage.style.display = 'none';
                defaultStylesPage.style.display = 'none';
                financePage.style.display = 'none';
                sectionsPage.style.display = 'block';
                break;
        }
    });
});