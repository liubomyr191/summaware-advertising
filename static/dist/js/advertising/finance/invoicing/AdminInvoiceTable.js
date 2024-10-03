const invoiceTable = document.querySelector('#invoice_table');
const invoiceTableBody = invoiceTable.getElementsByTagName('tbody')[0];

const tbodyRows = [...invoiceTableBody.rows];
const sendInvoiceBtns = document.querySelectorAll('.send-invoice-btn');

const sendInvoiceSubmitBtn = document.querySelector('#sendInvoice_submit_btn');

const serviceChargeTable = document.querySelector('#service_charge_table');
const serviceChargeTableBody = serviceChargeTable.getElementsByTagName('tbody')[0];

let totalCost = document.querySelector('#total_cost');

let accountId;
let orderId;
let invoiceAmount;
let chargeIds = [];
let printInvoiceCharge;

let isInsertionInvoice = false;
let insertionId;

const handleInvoiceBtnClick = (e) => {
    e.preventDefault();
    let row = e.target.parentElement.parentElement;

    let rowDataset = row.dataset;

    isInsertionInvoice = 'insertionInvoice' in rowDataset;
    insertionId = isInsertionInvoice ? rowDataset.insertionId : 0;

    invoiceAmount = row.children[4].textContent.split(' ')[1];

    accountId = rowDataset.accountId;
    orderId = rowDataset.orderId;

    $('#send_invoice_modal').modal('show');
}

sendInvoiceBtns.forEach(btn => {
    btn.addEventListener('click', handleInvoiceBtnClick);
});

function filterRows(orderId) {
    let newRows = isInsertionInvoice ? tbodyRows.filter(row => row.dataset.insertionId != insertionId) : tbodyRows.filter(row => row.dataset.orderId != orderId);
    let newRowIndexes = [];
    for (let i = 0; i < newRows.length; i++) {
        newRowIndexes.push(newRows[i].rowIndex)
    }
    for (let i = 0; i < invoiceTableBody.rows.length; i++) {
        let row = invoiceTableBody.rows[i];
        if (!(newRowIndexes.includes(row.rowIndex))) {
            invoiceTableBody.deleteRow(row.rowIndex - 1);
        }
    }
}

$('#send_invoice_modal').on('show.bs.modal', e => {
    let amountInput = document.querySelector('#send_invoice_form #amount');
    amountInput.value = Number(invoiceAmount);

    totalCost.textContent = invoiceAmount;

    fetch(`/advertising/ajax/service-charge/all/?account=${accountId}`, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            let serviceCharges = data.service_charges;

            populateServiceCharges(serviceCharges);
        });
});

$('#send_invoice_modal').on('hide.bs.modal', e => {
    let tableRows = [...serviceChargeTableBody.rows];
    tableRows.forEach(row => serviceChargeTableBody.removeChild(row))
});

sendInvoiceSubmitBtn.addEventListener('click', e => {
    let memoInput = document.querySelector('#memo');

    fetch(`/advertising/ajax/invoicing/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFTOKEN": getCookie('csrftoken')
        },
        body: JSON.stringify({
            "accountId": accountId,
            "orderId": orderId,
            "memo": memoInput.value,
            "serviceChargeList": chargeIds,
            "printInvoiceCharge": printInvoiceCharge,
            "invoiceCost": parseFloat(totalCost.textContent),
            "isInsertionInvoice": isInsertionInvoice,
            "insertionId": insertionId
        }),

    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error')) {
                alert(data.message);
                return;
            }
            alert(data.message)
            $('#send_invoice_modal').modal('hide');
            memoInput.value = '';
            filterRows(orderId);
        }).catch(error => console.error(error.message));
});

function populateServiceCharges(serviceCharges) {
    serviceCharges.forEach(charge => {
        let rows = '';
        if (charge.name == 'Mail Invoice Service Charge') {
            rows += `<tr>
                        <td><input type="checkbox" checked disabled/></td>
                        <td>${charge.name}</td>
                        <td>$ ${charge.amount}</td>
                        <td>${capitalize(charge.apply_level)}</td>
                    </tr>`;
            printInvoiceCharge = parseFloat(charge.amount);
            totalCost.textContent = parseFloat(totalCost.textContent) + parseFloat(charge.amount);
        } else {
            rows += `<tr data-charge-id=${charge.id}>
                        <td><input type="checkbox" class="add-charge-checkbox" /></td>
                        <td>${charge.name}</td>
                        <td>$ ${charge.amount}</td>
                        <td>${capitalize(charge.apply_level)}</td>
                    </tr>`;
        }
        $('#service_charge_table tbody').append(rows);
    });

    let checkboxes = [...document.querySelectorAll('.add-charge-checkbox')];
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', e => {
            let row = e.target.parentElement.parentElement;
            let id = row.dataset.chargeId;
            let chargeAmount = row.getElementsByTagName('td')[2].textContent.split(' ')[1];

            if (e.target.checked) {
                chargeIds.push(id);
                totalCost.textContent = parseFloat(totalCost.textContent) + parseFloat(chargeAmount);
            } else {
                chargeIds = chargeIds.filter(el => el != id)
                totalCost.textContent = parseFloat(totalCost.textContent) - parseFloat(chargeAmount);
            }
        });
    });
}

function capitalize(string) {
    const words = string.split(" ");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }
    return words.join(" ");
}