const userTable = document.querySelector('#user_table');
const userTableBody = userTable.getElementsByTagName('tbody')[0];
const userTableRows = [...userTableBody.getElementsByTagName('tr')];

const accountList = document.querySelector('#account_list');
const accountCheckboxes = [...document.querySelectorAll('.account-checkbox')];

let userId;

userTableRows.forEach(row => {
    row.addEventListener('click', (e) => {
        userId = e.target.parentElement.dataset.userId;

        fetch(`/advertising/admin/${userId}/account-access/`, {
            method: "GET"
        })
            .then(res => {
                if (!res.ok) {
                    alert(res.statusText);
                } else {
                    return res.json();
                }
            })
            .then(data => {
                if (data.message.includes('Error.')) {
                    alert(data.message);
                    return;
                } else {
                    let accountAccess = data.account_access;
                    accountCheckboxes.forEach(checkbox => checkbox.disabled = false);

                    accountAccess.forEach(accountId => {
                        accountCheckboxes.forEach(checkbox => {
                            let checkboxId = checkbox.id.split('-')[1];
                            if (accountId == checkboxId) checkbox.checked = true;
                        });
                    })
                }
            })
    })
});

function handleCheckboxClick(e) {
    let isChecked = e.target.checked;
    let accountId = e.target.id;

    fetch(`/advertising/admin/${userId}/account-access/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ isChecked, accountId, userId })
    })
        .then(res => {
            if (!res.ok) {
                alert(res.statusText);
            } else {
                return res.json();
            }
        })
        .then(data => {
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            }
        })
}

accountCheckboxes.forEach(checkbox => checkbox.addEventListener('click', handleCheckboxClick));