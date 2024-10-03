const userSearchInput = document.querySelector('#user_search');
const userCheckboxes = document.querySelectorAll('.user-checkbox');

let userId;

userCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('click', function (e) {
        let hasPermission = e.target.checked;
        userId = e.target.parentElement.dataset.userId;

        fetch(`/advertising/admin/permissions/custom-size/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userId, hasPermission })
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
    });
})