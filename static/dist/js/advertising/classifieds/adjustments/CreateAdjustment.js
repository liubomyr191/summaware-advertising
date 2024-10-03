const codeInput = document.querySelector('#code');
const descriptionInput = document.querySelector('#description');
const numberUnitsInput = document.querySelector('#number_units');
const amountInput = document.querySelector('#amount');
const valueTypeInput = document.querySelector('#value_type');
const applyLevelInput = document.querySelector('#applyLevel');
const creditDebitInput = document.querySelector('#credit_debit');
const publicationSelect = document.querySelector('#publication');

const createAdjustmentForm = document.querySelector('create_adjustment_form');
const createAdjustmentSubmit = document.querySelector('#create_adjustment_submit');

const handleCreate = e => {
    fetch(`/advertising/classifieds/adjustments/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "code": codeInput.value,
            "description": description.value,
            "amount": amount.value,
            "valueType": valueTypeInput.value,
            "applyLevel": getSelectedOption(applyLevelInput),
            "creditDebit": getSelectedOption(creditDebitInput),
            "publication": getSelectedOption(publicationSelect)
        }),
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            $('#create_adjustment_modal').modal('hide');
            window.location.reload();
        })
        .catch(err => {
            console.error(err);
            alert(err);
            return;
        })
}

createAdjustmentSubmit.addEventListener('click', handleCreate);