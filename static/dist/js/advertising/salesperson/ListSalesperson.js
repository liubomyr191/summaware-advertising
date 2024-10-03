const addFirstName = document.querySelector('#addFirstName');
const addLastName = document.querySelector('#addLastName');
const addCompany = document.querySelector('#addCompany');
const addEmail = document.querySelector('#addEmail');
const addPhone = document.querySelector('#addPhone');
const addAddress = document.querySelector('#addAddress');
const addCity = document.querySelector('#addCity');
const addState = document.querySelector('#addState');
const addZipCode = document.querySelector('#addZipCode');
const addCommission = document.querySelector('#addCommission');

const createSalespersonBtn = document.querySelector('#create_btn');

let salespersonId;

createSalespersonBtn.addEventListener('click', function (e) {
    fetch(`/advertising/salesperson/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            addFirstName: addFirstName.value,
            addLastName: addLastName.value,
            addCompany: addCompany.value,
            addEmail: addEmail.value,
            addPhone: addPhone.value,
            addAddress: addAddress.value,
            addCity: addCity.value,
            addState: addState.value,
            addZipCode: addZipCode.value,
            addCommission: addCommission.value
        })
    })
        .then(res => {
            if (!res.ok) {
                alert(res.statusText);
            } else {
                return res.json();
            }
        })
        .then(data => {
            console.log(data);
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                window.location.reload();
            }
        })
})