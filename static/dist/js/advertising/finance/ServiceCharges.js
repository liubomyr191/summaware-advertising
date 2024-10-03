const editChargeForm = document.querySelector('#edit_charge_form');
const editBtns = [...document.querySelectorAll('.edit-btn')];

const newChargeSubmitBtn = document.querySelector('#new_charge_submit_btn');
const editChargeSubmitBtn = document.querySelector('#edit_charge_submit_btn');

const nameInput = document.querySelector('#name');
const amountInput = document.querySelector('#amount');
const applyLevelInput = document.querySelector('#apply_level');

const editNameInput = document.querySelector('#edit_name');
const editAmountInput = document.querySelector('#edit_amount');
const editApplyLevelInput = document.querySelector('#edit_apply_level');
const editEnabledInput = document.querySelector('#edit_enabled');

const newAccountLock = document.querySelector('#new_locked');
const newAccountSelectBox = document.querySelector('#new_account_select');
const newAccountSelect = newAccountSelectBox.getElementsByTagName('select')[0];

const editAccountLock = document.querySelector('#edit_locked');
const editAccountSelectBox = document.querySelector('#edit_account_select');
const editAccountSelect = editAccountSelectBox.getElementsByTagName('select')[0];

let chargeId;
let accountId;

newChargeSubmitBtn.addEventListener('click', handleSubmit);
editChargeSubmitBtn.addEventListener('click', handleEditSubmit);
editBtns.forEach(btn => btn.addEventListener('click', handleEditBtnClick));

newAccountLock.addEventListener('click', e => {
    if (e.target.checked) {
        newAccountSelectBox.style.display = "block";
    } else {
        newAccountSelect.selectedIndex = 0;
        newAccountSelectBox.style.display = "none";
    }
});

newAccountSelect.addEventListener('change', e => {
    accountId = e.target.value == '' ? None : e.target.value;
});

editAccountLock.addEventListener('click', e => {
    if (e.target.checked) {
        editAccountSelectBox.style.display = "block";
    } else {
        editAccountSelect.selectedIndex = 0;
        editAccountSelectBox.style.display = "none";
    }
});

editAccountSelect.addEventListener('change', e => {
    accountId = e.target.value == '' ? null : e.target.value;
})

function handleSubmit(e) {
    if (!(nameInput.value.trim()) || !(amountInput.value) || !(applyLevelInput.value)) {
        alert('Please fill out all fields before submitting.');
        return;
    }

    fetch('/advertising/service-charges/new/', {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "name": nameInput.value.trim(),
            "amount": amountInput.value,
            "applyLevel": applyLevelInput.value,
            "account": accountId
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        alert(data.message);
        $('#new_charge_modal').modal('hide');
        window.location.reload();
    })
    .catch(err => {
        console.error(err);
        alert(err)
    });
}

function handleEditBtnClick(e) {
    let dataset = e.target.parentElement.parentElement.parentElement.dataset;
    chargeId = dataset.rowId;
    $('#edit_charge_modal').modal('show');
}

$('#edit_charge_modal').on('show.bs.modal', e => {
    accountId = null;
    fetch(`/advertising/ajax/service-charge/${chargeId}/`, {
        method: 'GET'
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        let serviceCharge = data.serviceCharge;
        populateEditForm(serviceCharge)
    });
})

function populateEditForm(serviceCharge) {
    let accountValue = null;
    editNameInput.value = serviceCharge.name;
    editAmountInput.value = serviceCharge.amount;
    editApplyLevelInput.value = serviceCharge.apply_level;
    editEnabledInput.checked = serviceCharge.enabled;

    editAccountLock.checked = false;
    editAccountSelectBox.style.display = 'none';
    
    if (serviceCharge.account != null) {
        editAccountLock.checked = true;
        editAccountSelectBox.style.display = 'block';
        
        accountValue = serviceCharge.account;
        let foundOption = [...editAccountSelect.options].find(option => option.value == accountValue);
        if (foundOption) { foundOption.selected = true }
    }
}

function handleEditSubmit(e) {
    fetch(`/advertising/service-charges/${chargeId}/edit/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "name": editNameInput.value.trim(),
            "amount": editAmountInput.value,
            "applyLevel": editApplyLevelInput.value,
            "enabled": editEnabledInput.checked,
            "account": accountId
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        alert(data.message);
        $('#edit_charge_modal').modal('hide');
        window.location.reload();
    })
    .catch(err => {
        console.error(err);
        alert(err)
    })
}