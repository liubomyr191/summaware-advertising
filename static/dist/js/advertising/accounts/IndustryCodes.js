const createBtn = document.querySelector('#create_new_btn');
const cancelBtn = document.querySelector('#cancel_btn');
const plusBtn = document.querySelector('#new_code_plus');

const searchBtn = document.querySelector('#code_search');
const searchInput = document.querySelector('#code_search_input');

const codesTable = document.querySelector('#industry_codes_table');

const codesTableBody = codesTable.getElementsByTagName('tbody')[0];
const tableRows = [...codesTableBody.getElementsByTagName('tr')];

const newCodeFormSection = document.querySelector('#new_code_form_section');

const editCodeFormSection = document.querySelector('#edit_code_form_section');
const editCodeInput = document.querySelector('input[name="editCode"]')
const editDescriptionInput = document.querySelector('textarea[name="editDescription"]')
const editCodeSubmitBtn = document.querySelector('#edit_code_submit');

const editIcons = document.querySelectorAll('.edit-icon');
const deleteIcons = document.querySelectorAll('.delete-icon');

let codeActive;
let codeId;
let codeNumber;
let codeDescription;
let icons;

$(document).ready(() => {
    newCodeFormSection.style.display = 'none';
    editCodeFormSection.style.display = 'none';
})

const handleClickNew = e => {
    newCodeFormSection.style.display = 'flex';

    createBtn.style.display = 'none';
    editCodeFormSection.style.display = 'none';
}

const handleCancelClick = e => {
    createBtn.style.display = 'block';

    newCodeFormSection.style.display = 'none';
    editCodeFormSection.style.display = 'none';
}

const handleEdit = e => {
    e.preventDefault();

    console.log(codeId.textContent);
    console.log(codeDescription.textContent);
    console.log(codeNumber.textContent);

    // fetch(`/advertising/account/${accountId}/industry-codes/${codeId}/edit`, {
    //     method: "POST",
    //     credentials: "same-origin",
    //     headers: {
    //         "X-CSRFToken": getCookie('csrftoken'),
    //         "Accept": "application/json",
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({
    //         active: codeActive,
    //         codeId: codeId,
    //         codeNumber: codeNumber,
    //         codeDescription: codeDescription
    //     })
    // })
}

const toggleSearch = e => {
    if (searchInput.style.display == 'block') {
        searchInput.style.display = 'none';
    } else {
        searchInput.style.display = 'block';
    }
}

const handleSearch = e => {
    let searchTerm = e.target.value;

    for (let i = 0; i < tableRows.length; i++) {
        rowContent = tableRows[i].getElementsByTagName('td');

        for (let j = 0; j < rowContent.length; j++) {
            cellContent = rowContent[j];

            if (cellContent.textContent.toLowerCase().indexOf(searchTerm) > -1) {
                tableRows[i].style.display = "";
                break;
            } else {
                tableRows[i].style.display = "none";
            }
        }
    }
}

editIcons.forEach(icon => icon.addEventListener('click', e => {
    editCodeFormSection.style.display = 'flex';
    createBtn.style.display = 'none';
    newCodeFormSection.style.display = 'none';

    let parentElement = e.target.parentElement.parentElement;

    [codeId, codeDescription, codeNumber, icons] = [...parentElement.children];

    editCodeInput.value = codeNumber.textContent;
    editDescriptionInput.value = codeDescription.textContent;

}))

createBtn.addEventListener('click', handleClickNew);
plusBtn.addEventListener('click', handleClickNew);
cancelBtn.addEventListener('click', handleCancelClick);
searchBtn.addEventListener('click', toggleSearch);
searchInput.addEventListener('keyup', handleSearch);
editCodeSubmitBtn.addEventListener('click', handleEdit);