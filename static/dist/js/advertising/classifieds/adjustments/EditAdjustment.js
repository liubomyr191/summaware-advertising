const editAdjustmentBtns = document.querySelectorAll('.edit-adjustment-btn');

const editAdjustmentModal = document.querySelector('#edit_adjustment_modal');
const editAdjustmentForm = document.querySelector('#edit_adjustment_form');

const editAdjustmentCode = document.querySelector('#editCode');
const editAdjustmentDescription = document.querySelector('#editDescription');
const editAdjustmentAmount = document.querySelector('#editAmount');
const editAdjustmentValueType = document.querySelector('#editValueType');
const editApplyLevel = document.querySelector('#editApplyLevel');
const editCreditDebit = document.querySelector('#editCreditDebit');
const editPublication = document.querySelector('#editPublication');
const editActive = document.querySelector('#editActive');

const editAdjustmentSubmitBtn = document.querySelector('#edit_adjustment_submit');

let adjustmentId;
let url;

const showEditModal = e => {
    let row = e.target.parentElement;
    let rowDataset = row.dataset;

    adjustmentId = rowDataset.adjustmentId;

    if (adjustmentId == undefined) {
        alert('Error. Cannot access adjustment details.');
        return;
    }

    url = `/advertising/classifieds/adjustments/${adjustmentId}/`;

    $('#edit_adjustment_modal').modal('show');
};
$('#edit_adjustment_modal').on('show.bs.modal', e => {
    fetch(url, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            if (data.adjustment_details) {
                let details = data.adjustment_details;

                editAdjustmentCode.value = details.code;
                editAdjustmentDescription.value = details.description;
                editAdjustmentAmount.value = details.amount;
                selectOption(editAdjustmentValueType, details.value_type);
                selectOption(editApplyLevel, details.apply_level);
                selectOption(editCreditDebit, details.type);
                selectOption(editPublication, details.publication)

                editActive.checked = details.active;
            } else {
                alert('An error occurred trying to get adjustment details. Please try again.');
                return;
            }
        })
        .catch(err => {
            console.error(err)
            alert(err);
        })
});

const handleEditSubmit = e => {
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "editCode": editAdjustmentCode.value,
            "editDescription": editAdjustmentDescription.value,
            "editAmount": editAdjustmentAmount.value,
            "editValueType": getSelectedOption(editAdjustmentValueType),
            "editApplyLevel": getSelectedOption(editApplyLevel),
            "editCreditDebit": getSelectedOption(editCreditDebit),
            "editPublication": getSelectedOption(editPublication),
            "editActive": editActive.checked
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error')) {
                alert(data.message);
                return;
            }

            $('#edit_adjustment_modal').modal('hide');
            window.location.reload();
        })
}

editAdjustmentBtns.forEach(btn => btn.addEventListener('click', showEditModal));
editAdjustmentSubmitBtn.addEventListener('click', handleEditSubmit);