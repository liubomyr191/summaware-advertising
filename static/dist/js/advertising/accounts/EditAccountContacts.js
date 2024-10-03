const editFirstNameInput = document.querySelector('#editFirstName');
const editLastNameInput = document.querySelector('#editLastName');
const editEmailInput = document.querySelector('#editEmail');
const editPhoneInput = document.querySelector('#editPhone');
const editDepartmentInput = document.querySelector('#editDepartment');
const editActiveInput = document.querySelector('#editActive');
const editDefaultInput = document.querySelector('#editDefault');

const editContactForm = document.querySelector('#edit_contact_form');

const editContactBtns = document.querySelectorAll('.edit-account-contact');
const editContactSubmitBtn = document.querySelector('#edit_contact_submit');

let contactId = 0;

const handleEditBtnClick = e => {
    let parentRow = e.target.parentElement.parentElement.parentElement;
    let rowDataset = parentRow.dataset;

    contactId = rowDataset.id;

    $('#edit_account_contact_modal').modal('show');
}

$('#edit_account_contact_modal').on('show.bs.modal', e => {
    if ((contactId != undefined) && (accountId != undefined)) {
        fetch(`/advertising/account/${accountId}/contacts/${contactId}`, {
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

                editFirstNameInput.value = first_name;
                editLastNameInput.value = last_name;
                editEmailInput.value = email;
                editPhoneInput.value = phone_number;
                editDepartmentInput.value = department;
                editActiveInput.checked = active;
                editDefaultInput.checked = defaultValue;

            })
            .catch(err => console.log(err));
    }
});

const handleEditSubmit = e => {
    fetch(`/advertising/account/${accountId}/contacts/${contactId}/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "firstName": editFirstNameInput.value,
            "lastName": editLastNameInput.value,
            "email": editEmailInput.value,
            "phone": editPhoneInput.value,
            "department": editDepartmentInput.value,
            "active": editActiveInput.checked,
            "default": editDefaultInput.checked
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error.')) {
                alert('data.message');
            } else {
                $('edit_account_contact_modal').modal('hide');
                window.location.reload();
            }
        })
        .catch(err => console.log(err));
}

$('#edit_account_contact_modal').on('hide.bs.modal', function (e) {
    $(this).find("input,textarea,select").val('');
    $(this).find("input[type=checkbox], input[type=radio]").prop("checked", "");
});

editContactBtns.forEach(btn => btn.addEventListener('click', handleEditBtnClick));
editContactSubmitBtn.addEventListener('click', handleEditSubmit);

const getCookie = name => {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}