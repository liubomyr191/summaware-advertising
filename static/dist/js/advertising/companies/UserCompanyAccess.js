const userCheckboxes = document.querySelectorAll('.user-checkbox');
const companySelect = document.querySelector('#companySelect');

let companyId;
let userId;

window.addEventListener("load", (event) => {
    userCheckboxes.forEach(checkbox => checkbox.disabled = true);
});

companySelect.addEventListener('change', e => {
    userCheckboxes.forEach(checkbox => checkbox.disabled = false);
    companyId = e.target.value;

    if (companyId == '') {
        userCheckboxes.forEach(checkbox => {
            checkbox.disabled = true;
            checkbox.checked = false;
        })
    } else {
        fetch(`/advertising/admin/company/user-access/?companyId=${companyId}`, {
            method: 'GET'
        })
            .then(res => res.json())
            .then(data => {
                let userList = data.user_list;

                userCheckboxes.forEach(checkbox => {
                    let userId = checkbox.parentElement.dataset.userId;
                    if (userList.includes(Number(userId))) {
                        checkbox.checked = true;
                    }
                });
            });
    }
});

const handleAccessChange = e => {
    userId = e.target.parentElement.dataset.userId;
    let hasAccess = e.target.checked;

    fetch('/advertising/admin/company/user-access/', {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            userId,
            companyId,
            hasAccess
        })
    })
        .then(res => res.json())
        .then(data => {
            // console.log(data);
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            }
        })
        .catch(err => console.error(err.statusText))
}

userCheckboxes.forEach(checkbox => checkbox.addEventListener('change', handleAccessChange));