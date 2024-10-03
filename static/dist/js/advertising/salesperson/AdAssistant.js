const adAssistantModal = document.querySelector('#add_ad_assistant_modal');
const adAssistantCheckboxes = document.querySelectorAll('.ad-assistant-checkbox');
const adAssistantSubmitBtn = document.querySelector('#add_assistant_submit');

let adAssistants = [];
let userId;

let url = `/advertising/salesperson/${salespersonId}/ad-assistants/`;

$('#add_ad_assistant_modal').on('show.bs.modal', function (e) {
    fetch(url, {
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
            console.log(data)
            if (data.ad_assistants) {
                let assistants = data.ad_assistants;
                adAssistantCheckboxes.forEach(checkbox => {
                    let userId = checkbox.parentElement.dataset.userId;
                    assistants.forEach(assistant => {
                        checkbox.checked = assistant.user == userId;
                    })
                });
            }
        });
});

$('#add_ad_assistant_modal').on('hide.bs.modal', function (e) {
    adAssistants = [];
});

// adAssistantCheckboxes.forEach(checkbox => {
//     checkbox.addEventListener('click', function (e) {
//         userId = e.target.parentElement.dataset.userId;

//         if (e.target.checked) {
//             adAssistants.push(userId);
//         } else {
//             adAssistants = adAssistants.filter(elem => elem != userId);
//         }
//     });
// })

adAssistantSubmitBtn.addEventListener('click', function (e) {
    adAssistantCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            adAssistants.push(checkbox.parentElement.dataset.userId);
        }
    })
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ adAssistants, salespersonId })
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
                $('#add_ad_assistant_modal').modal('hide');
                window.location.reload();
            }
        });
})