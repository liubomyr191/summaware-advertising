const editBtns = document.querySelectorAll('.edit-btn');
const editForm = document.querySelector('#edit_invoice_form')
const submitBtn = document.querySelector('#edit_submit_btn');

let billEndInput = document.querySelector('#bill_end');
let amountInput = document.querySelector('#amount');
let memoInput = document.querySelector('#memo');

let invoiceId;

const handleClick = e => {
    let dataset = e.target.parentElement.parentElement.dataset;
    invoiceId = dataset.id;

    // TODO - make this a GET request
    fetch('/advertising/ajax/invoice/details/', {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "invoiceId": invoiceId }),

    })
    .then(response => response.json())
    .then(data => {
        let invoiceDetails = data.invoice;

        billEndInput.value = invoiceDetails.bill_end;
        amountInput.value = invoiceDetails.amount;
        memoInput.value = invoiceDetails.memo;
    });
}

const handleSubmit = e => {
    fetch(editForm.action, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "id": invoiceId,
            "bill_end": billEndInput.value,
            "amount": amountInput.value,
            "memo": memoInput.value
        })
    });
}

editBtns.forEach(btn => {
    btn.addEventListener('click', handleClick);
});

submitBtn.addEventListener('click', handleSubmit);