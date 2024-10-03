const overrideBtns = [...document.querySelectorAll('.override-btn')];
const overrideTable = document.querySelector('#manager_override_table');
const overrideTableBody = overrideTable.getElementsByTagName('tbody')[0];
const tbodyRows = [...overrideTableBody.getElementsByTagName('tr')];

const handleOverride = e => {
    let parentRow = e.target.parentElement.parentElement;

    let rowDataArray = parentRow.getElementsByTagName('td');
    let orderId = rowDataArray[0].textContent;
    let accountId = rowDataArray[1].textContent;
    let managerId = rowDataArray[2].textContent;

    let isConfirmed = confirm('Are you sure you want to override the order?');
    if (!isConfirmed) return;

    fetch('/advertising/ajax/manager-overrides/credit-limits/', {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "orderId": orderId,
            "accountId": accountId,
            "managerId": managerId
         })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        alert(data.message);
    })
    .catch(err => console.error(err))
}

overrideBtns.forEach(btn => btn.addEventListener('click', handleOverride));

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    });
    return cookie[name];
}