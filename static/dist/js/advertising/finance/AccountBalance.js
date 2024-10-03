const payAmountInput = document.querySelector('#pay_amount');
const accountBalanceSubmit = document.querySelector('#account_balance_submit');
const goesToInput = document.querySelector('#goes_to');

let latestAmount;
let oldestAmount;

const handleBalanceSubmit = e => {
    e.preventDefault();
    if ((payAmountInput.value == '') || (payAmountInput.value == 0) || (goesToInput.value == '')) {
        alert('You must enter a value and tell where it should go to.');
        return;
    }
    let hasError;

    switch (goesToInput.value) {
        case 'latest_invoice':
            if (payAmountInput.value > parseFloat(latestAmount)) { 
                alert('Error. Amount entered exceeds the amount of the latest invoice.');
                hasError = true;
            }
            break; 
        case 'oldest_invoice':
            if (payAmountInput.value > parseFloat(oldestAmount)) { 
                alert('Error. Amount entered exceeds the amount of the oldest invoice.');
                hasError = true;
            }
            break;  
    }

    if (hasError) { return; }

    fetch(`/advertising/account/${account_id}/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "type": "account_balance",
            "amount": parseFloat(payAmountInput.value),
            "goesTo": goesToInput.value
        }),
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        $('#account_balance_modal').modal('hide');
        window.location.reload();
    });
}

accountBalanceSubmit.addEventListener('click', handleBalanceSubmit);

$('#account_balance_modal').on('show.bs.modal', e => {

    // fetch(`/advertising/ajax/invoice/details?reqType=invoice_details&account=${account_id}`, {
    //     method: "GET",
    //     credentials: "same-origin",
    //     headers: {
    //         "Accept": "application/json",
    //         'Content-Type': 'application/json'
    //     }
    // })
    // .then(res => res.json())
    // .then(data => {
    //     console.log(data)
    // });
});

$('#account_balance_modal').on('hide.bs.modal', e => {
    payAmountInput.value = '';
    goesToInput.value = '';
});