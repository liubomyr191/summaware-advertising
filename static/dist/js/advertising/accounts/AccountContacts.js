const editContactBtns = document.querySelectorAll('.edit-account-contact');
const editContactSubmitBtn = document.querySelector('#edit_contact_submit');

const firstNameInput = document.querySelector('#firstName');
const lastNameInput = document.querySelector('#lastName');
const emailInput = document.querySelector('#email');
const phoneInput = document.querySelector('#phone');
const departmentInput = document.querySelector('#department');
const activeInput = document.querySelector('#active');
const defaultInput = document.querySelector('#default');

let contactId;

const handleEditBtnClick = e => {
    const row = e.target.parentElement.parentElement;
    const rowDataset = row.dataset;

    contactId = rowDataset.contactId;

    $('#edit_account_contact_modal').modal('show');
}

const handleSubmit = e => {
    e.preventDefault();

    fetch(`/advertising/account/${account_id}/contacts/${contactId}/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "firstName": firstNameInput.value,
            "lastName": lastNameInput.value,
            "email": emailInput.value,
            "phone": phoneInput.value,
            "department": departmentInput.value,
            "active": activeInput.checked,
            "default": defaultInput.checked,
        }),
    })
        .then(res => res.json())
        .then(data => {
            $('#edit_account_contact_modal').modal('hide');
            window.location.reload();
        })
        .catch(err => console.log(err))
}

$('#edit_account_contact_modal').on('show.bs.modal', e => {
    if ((contactId != undefined) && (account_id != undefined)) {
        fetch(`/advertising/account/${account_id}/contacts/${contactId}`, {
            method: "GET",
            credentials: "same-origin",
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json'
            }
        })
            .then(res => res.json())
            .then(data => {
                const contactDetails = data.contact;

                let { first_name, last_name, email, phone_number, department, default: defaultValue, active } = contactDetails;

                firstNameInput.value = first_name;
                lastNameInput.value = last_name;
                emailInput.value = email;
                phoneInput.value = phone_number;
                departmentInput.value = department;
                activeInput.checked = active;
                defaultInput.checked = defaultValue;

            })
            .catch(err => console.log(err))
    }
})

editContactBtns.forEach(btn => btn.addEventListener('click', handleEditBtnClick));
editContactSubmitBtn.addEventListener('click', handleSubmit);