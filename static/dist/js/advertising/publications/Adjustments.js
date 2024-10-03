const createCode = document.querySelector('#adjustment_code');
const createDescription = document.querySelector('#adjustment_description');
const createApplyLevel = document.querySelector('#adjustment_apply_level');
const createValueType = document.querySelector('#adjustment_value_type');
const createAmount = document.querySelector('#adjustment_amount');
const createType = document.querySelector('#adjustment_type');
const createSection = document.querySelector('#adjustment_section');
const createPrompt = document.querySelector('#adjustment_prompt_value');
const createGrossNet = document.querySelector('#adjustment_gross_net');

const createSubmitBtn = document.querySelector('#create_adjustment_submit');

const editCode = document.querySelector('#edit_adjustment_code');
const editDescription = document.querySelector('#edit_adjustment_description');
const editApplyLevel = document.querySelector('#edit_adjustment_apply_level');
const editValueType = document.querySelector('#edit_adjustment_value_type');
const editAmount = document.querySelector('#edit_adjustment_amount');
const editType = document.querySelector('#edit_adjustment_type');
const editSection = document.querySelector('#edit_adjustment_section');
const editPrompt = document.querySelector('#edit_adjustment_prompt_value');
const editActive = document.querySelector('#edit_adjustment_active');
const editGrossNet = document.querySelector('#edit_gross_net');

const editSubmitBtn = document.querySelector('#edit_adjustment_submit');

const editAdjustmentBtns = document.querySelectorAll('.edit-adjustment');

let adjustmentId;

createSubmitBtn.addEventListener('click', function (e) {
    e.preventDefault();
    if (!createCode.value || !createDescription.value || !createApplyLevel || !createValueType
        || !createAmount.value || !createType) {
        alert('Please fill out all of the required fields');
        return;
    } else {
        fetch(`/advertising/publication/${publication_id}/adjustments/new/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: createCode.value,
                description: createDescription.value,
                apply_level: getSelectedOption(createApplyLevel),
                value_type: getSelectedOption(createValueType),
                amount: createAmount.value,
                type: getSelectedOption(createType),
                prompt_for_value: createPrompt.checked,
                section: getSelectedOption(createSection),
                grossNet: getSelectedOption(createGrossNet)
            })
        })
            .catch(err => console.error(err))
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
                    $('#create_adjustment_modal').modal('hide');
                    window.location.reload();
                }
            });
    }


});

editAdjustmentBtns.forEach(btn => btn.addEventListener('click', e => {
    adjustmentId = e.target.dataset.adjustmentId;
    if (adjustmentId) $('#edit_adjustment_modal').modal('show');
}));

$('#edit_adjustment_modal').on('show.bs.modal', e => {
    if (adjustmentId) {
        fetch(`/advertising/publication/${publication_id}/adjustments/${adjustmentId}/`, {
            method: "GET"
        })
            .catch(err => console.error(err))
            .then(res => {
                if (!res.ok) {
                    alert(res.statusText);
                } else {
                    return res.json();
                }
            })
            .then(data => {
                if (data.adjustment) {
                    let adjustment = data.adjustment;

                    editCode.value = adjustment.code;
                    editDescription.value = adjustment.description;

                    selectOption(editApplyLevel, adjustment.apply_level);
                    selectOption(editValueType, adjustment.value_type);

                    editAmount.value = adjustment.amount;

                    selectOption(editType, adjustment.type);

                    editPrompt.checked = adjustment.prompt_for_value;
                    editActive.checked = adjustment.active;

                    selectOption(editGrossNet, adjustment.gross_net);

                    if (adjustment.section) {
                        selectOption(editSection, adjustment.section)
                    }
                }
            });
    } else {
        alert('Error. Cannot find the adjustment details. Please try again.');
        $('#edit_adjustment_modal').modal('hide');
        return;
    }
})

editSubmitBtn.addEventListener('click', e => {
    if (adjustmentId) {
        fetch(`/advertising/publication/${publication_id}/adjustments/${adjustmentId}/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: editCode.value,
                description: editDescription.value,
                apply_level: getSelectedOption(editApplyLevel),
                value_type: getSelectedOption(editValueType),
                amount: editAmount.value,
                type: getSelectedOption(editType),
                prompt_for_value: editPrompt.checked,
                section: getSelectedOption(editSection),
                active: editActive.checked,
                grossNet: getSelectedOption(editGrossNet)
            })
        })
            .catch(err => console.error(err))
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
                    $('#edit_adjustment_modal').modal('hide');
                    window.location.reload();
                }
            });
    }
});