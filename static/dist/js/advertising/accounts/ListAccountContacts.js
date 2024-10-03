const addContactBtn = document.querySelector('#add_btn');

const accountContact = document.querySelectorAll('.item');

const addContactFormSection = document.querySelector('#create_account_contact');
const addContactForm = addContactFormSection.getElementsByTagName('form')[0];
const addFormSubmitBtn = document.querySelector('#create_contact_submit');
const addFormCancelBtn = document.querySelector('#create_contact_cancel');

const newCompanyContactSection = document.querySelector('#new_company_contact_section');
const newCompanyContactBtn = document.querySelector('#new_company_contact_btn');

const editContactFormSection = document.querySelector('#edit_account_contact');
const editContactSubmitBtn = document.querySelector('#edit_contact_submit');

const editIcons = document.querySelectorAll('.edit-icon');
const deleteIcons = document.querySelectorAll('.delete-icon');

const editFirstName = document.querySelector('#editFirstName');
const editLastName = document.querySelector('#editLastName');
const editEmail = document.querySelector('#editEmail');
const editDepartment = document.querySelector('#editDepartment');
const editPhone = document.querySelector('#editPhone');
const editDefault = document.querySelector('#editDefault');
const editActive = document.querySelector('#editActive');

const itemIcons = document.querySelectorAll('.item-icons');

let contactId;

$(document).ready(() => {
    addContactFormSection.style.display = 'none';
    editContactFormSection.style.display = 'none';
});

addContactBtn.addEventListener('click', e => {
    if (addContactFormSection.style.display == 'none') {
        addContactFormSection.style.display = 'block';
        newCompanyContactSection.style.display = 'none';
    } else {
        addContactFormSection.style.display = 'none';
        newCompanyContactSection.style.display = 'block';
    }

});

newCompanyContactBtn.addEventListener('click', e => {
    newCompanyContactSection.style.display = 'none';
    addContactFormSection.style.display = addContactFormSection.style.display == 'none' ? 'block' : 'none';
});

addFormSubmitBtn.addEventListener('click', e => {
    e.preventDefault();

    let formData = $('#create_contact_form').serializeArray();

    fetch(`/advertising/account/${accountId}/company-contacts/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            formData,
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            if (data.message.includes('Error')) {
                console.error(data.message);
                alert(data.message);
            } else {
                window.location.reload();
            }
        });
})

addFormCancelBtn.addEventListener('click', e => {
    addContactFormSection.style.display = 'none';
    newCompanyContactSection.style.display = 'block';
});

editIcons.forEach(icon => {
    icon.addEventListener('click', e => {
        contactId = e.target.parentElement.dataset.contactId;

        fetch(`/advertising/account/${accountId}/company-contacts/${contactId}/`, {
            method: "GET"
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                if (data.message.includes('Error')) {
                    console.error(data.message);
                    alert(data.message);
                } else {
                    newCompanyContactSection.style.display = 'none';
                    editContactFormSection.style.display = 'block';

                    let contactDetails = data.contact;

                    editFirstName.value = contactDetails.first_name;
                    editLastName.value = contactDetails.last_name;
                    editEmail.value = contactDetails.email;
                    editDepartment.value = contactDetails.department;
                    editPhone.value = contactDetails.phone_number;
                    editActive.checked = contactDetails.active;
                    editDefault.checked = contactDetails.default;
                }
            })

    })
});

editContactSubmitBtn.addEventListener('click', e => {
    e.preventDefault();

    fetch(`/advertising/account/${accountId}/company-contacts/${contactId}/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            firstName: editFirstName.value,
            lastName: editLastName.value,
            email: editEmail.value,
            phone: editPhone.value,
            department: editDepartment.value,
            default: editDefault.checked,
            active: editActive.checked
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error')) {
                console.error(data.message);
                alert(data.message);
                return;
            } else {
                window.location.reload();
            }
        })
});

deleteIcons.forEach(icon => {
    icon.addEventListener('click', e => {
        contactId = e.target.parentElement.dataset.contactId;

        let confirmation = confirm('Are you sure you want to delete this contact?');

        if (confirmation) {
            fetch(`/advertising/account/${accountId}/company-contacts/${contactId}/action`, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "Accept": "application/json",
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: "delete"
                })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.message.includes('Error')) {
                        console.error(data.message);
                        alert(data.message);
                        return;
                    } else {
                        window.location.reload();
                    }
                })
        }
    })
})