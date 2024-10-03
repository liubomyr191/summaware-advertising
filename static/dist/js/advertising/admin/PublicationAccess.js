const userTable = document.querySelector('#user_table');
const userTbody = userTable.getElementsByTagName('tbody')[0];
const userTbodyRows = [...userTbody.getElementsByTagName('tr')];

const publicationList = document.querySelector('#publication_list');
const publicationInputs = publicationList.getElementsByTagName('input');

let userId;

const handleUserClick = e => {
    let parentRow = e.target.parentElement;
    let dataset = parentRow.dataset;

    userId = dataset.id;

    fetch(`/advertising/admin/${userId}/publication-access/`, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error')) {
                alert(data.message);
            } else {
                for (let input of publicationInputs) {
                    input.disabled = false;
                    input.addEventListener('click', handlePublicationClick)
                }
                populateCheckboxes(data.publication_access)
            }
        });
}

const handlePublicationClick = e => {
    let isChecked = e.target.checked;
    let publication = e.target.id;

    fetch(`/advertising/admin/${userId}/publication-access/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            publication,
            isChecked
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error')) {
                console.error(data.message);
                alert(data.message);
            }
            populateCheckboxes(data.publication_access);
        })
}

const populateCheckboxes = publications => {
    let pubList = [];
    for (let [key, value] of Object.entries(publications)) {
        pubList.push(value)
    }

    for (let input of publicationInputs) {
        let inputId = input.id.split('-')[1];
        for (let pubId of pubList) {
            if (inputId == pubId) input.checked = true;
        }
    }
}

for (const row in userTbodyRows) {
    userTbodyRows[row].children[0].addEventListener('click', handleUserClick);
}

const getCookie = name => {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}