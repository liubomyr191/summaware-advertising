const companySelect = document.querySelector('#company_select');
const companyRateTable = document.querySelector('#company_rate_table');
const rateCheckboxes = document.querySelectorAll('.rate-checkbox');

$(document).ready(function (e) {
    rateCheckboxes.forEach(checkbox => {
        checkbox.disabled = true;
    });
});

companySelect.addEventListener('change', function (e) {
    rateCheckboxes.forEach(checkbox => {
        checkbox.disabled = e.target.value == '' ? true : false;
    });

    // TODO - get all the company rates and check the box if the rate exists
});

// ? if the user unchecks the box, should the company rate get deleted or just marked as inactive?