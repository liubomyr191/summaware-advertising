const payInvoiceBtns = [...document.querySelectorAll('.pay-invoice-btn')];
const invoiceAmount = document.querySelector('#invoice_amount');

const invoiceDetailModal = document.querySelector('#invoice_detail_modal');

const invoiceIdHeader = document.querySelector('#invoiceDetails_id');
const invoiceAmountHeader = document.querySelector('#invoiceDetails_amount');
const invoiceMemoField = document.querySelector('#invoiceDetails_memo');
const invoiceTotal = document.querySelector('#invoiceDetails_total');

let invoiceId;

payInvoiceBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        let dataset = e.target.parentElement.parentElement.dataset;
        invoiceId = dataset.invoiceId;

        $('#pay_invoice_modal').modal('show');

        let row = e.target.parentElement.parentElement;
        let amount = row.getElementsByTagName('td')[1].textContent;

        let payFullCheckbox = document.querySelector('#pay_full');
        let payOtherInput = document.querySelector('#pay_other');
        let useCreditInput = document.querySelector('#use_credit');

        let submitBtn = document.querySelector('#pay_invoice_submit');

        invoiceAmount.textContent = `(${amount})`;

        payFullCheckbox.addEventListener('input', e => {
            if (e.target.checked) payOtherInput.value = '';
        });

        payOtherInput.addEventListener('input', e => {
            if (payOtherInput.value != '') payFullCheckbox.checked = false;
        })

        submitBtn.addEventListener('click', e => {
            if ((payOtherInput.value == '') && 
                (payFullCheckbox.checked == false) && 
                (useCreditInput.checked == false)) {
                    alert('Please choose a payment option')
                    return;
            } 

            let amount;
            if (payFullCheckbox.checked) {
                amount = 'full';
            } else if (payOtherInput.value != '') {
                amount = payOtherInput.value;
            } else if (useCreditInput.checked) {
                amount = 'use_credit';
            }

            fetch(`/advertising/invoice/${invoiceId}/pay/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "Accept": "application/json",
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    "type": "pay",
                    "amount": amount
                })
            })
            .then(res => res.json())
            .then(data => {
                // TODO - once the JSON is returned, reload just the tables, may have to delete and remake them
                $('#pay_invoice_modal').modal('hide');
                payOtherInput.value = '';
                payFullCheckbox.checked = false;
            })
            .catch(err => {
                console.error(err);
                alert('An error occurred while processing the payment')
            })
        })
    })
});

$('#pay_invoice_modal').on('show.bs.modal', e => {
    // TODO - refactor this to be only one ajax request

    console.log(invoiceId)
    fetch(`/advertising/ajax/invoice/details/?invoiceId=${invoiceId}`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => { 
        populateInvoiceDetailModal(data)
    })
    .catch(err => {
        console.error(err);
        alert(err)
        return;
    });
});

$('#pay_invoice_modal').on('hide.bs.modal', e => {
    $('#invoice_detail_table tbody').empty();
});

function populateInvoiceDetailModal(data) {
    let invoiceDetails = data.invoice;
    let serviceCharges = data.service_charges;

    invoiceIdHeader.textContent = `Invoice #${invoiceDetails.id}`;
    invoiceAmountHeader.textContent = `Original Amount: $${invoiceDetails.original_amount.toFixed(2)}`;

    // TODO - fix this amount (some paid invoice totals are showing incorrect amounts)
    invoiceTotal.textContent = `Total: $${invoiceDetails.amount}`;

    let tbodyRows = '';
    for (let i = 0; i < serviceCharges.length; i++) {
        let service_charge = serviceCharges[i];
        tbodyRows += `<tr>
                        <td>${service_charge.name}</td>
                        <td>${service_charge.amount.toFixed(2)}</td>
                    </tr>`;
    }
    $('#invoice_detail_table tbody').append(tbodyRows);
}

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}