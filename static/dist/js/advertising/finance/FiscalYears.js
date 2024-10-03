const fiscalYearsModal = document.querySelector('#new_fiscal_year_modal');
const fiscalYearsForm = document.querySelector('#new_fiscal_year_form');
const fiscalYearsSubmitBtn = document.querySelector('#fiscal_year_submit_btn')

let fyDescription = document.querySelector('#description');
let fyStartDate = document.querySelector('#start_date');
let fyEndDate = document.querySelector('#end_date');

const accountPeriodModal = document.querySelector('#new_accounting_period_modal');
const accountPeriodForm = document.querySelector('#new_accounting_period_form');
const accountPeriodSubmitBtn = document.querySelector('#accounting_period_submit_btn');

let apCode = document.querySelector('#apCode');
let apName = document.querySelector('#apName');
let apStartDate = document.querySelector('#apStartDate');
let apEndDate = document.querySelector('#apEndDate');

const fiscalYearsTable = document.querySelector('#fiscal_year_table');
const fiscalYearsTbody = fiscalYearsTable.getElementsByTagName('tbody')[0];

const accountingPeriodTable = document.querySelector('#accounting_period_table');
const accountingPeriodTbody = accountingPeriodTable.getElementsByTagName('tbody')[0];

const viewInvoicesTable = document.querySelector('#view_invoices_table');
const viewInvoicesTableBody = viewInvoicesTable.getElementsByTagName('tbody')[0];

const accountId = window.location.pathname.split('/')[3];

const calendarYearToggle = document.querySelector('#toggle_calendar_year');

var fiscalYear;

let viewInvoiceBtns;
let url = `/advertising/account/${accountId}/fiscal-years/`;

$(document).ready(() => {
    $('#code').trigger('click');
})

const handleCalendarYearToggle = e => {
    let isChecked = e.target.checked;

    if (isChecked) {
        fyStartDate.value = `${(new Date().getFullYear())}-01-01`;
        fyEndDate.value = `${(new Date().getFullYear())}-12-31`;
    } else {
        fyStartDate.value = '';
        fyEndDate.value = '';
    }
}

const handleFiscalYearsSubmit = (e) => {
    e.preventDefault();

    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "description": fyDescription.value,
            "startDate": fyStartDate.value,
            "endDate": fyEndDate.value,
            "accountId": accountId,
            "type": "fiscal_year"
        }),
    }).then((res) =>{
        console.log(res);
        window.location.reload();
    }).catch(err => {
        alert(err.message)
    })
}

const handleAccountingPeriodSubmit = (e) => {
    e.preventDefault();

    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "code": apCode.value,
            "name": apName.value,
            "startDate": apStartDate.value,
            "endDate": apEndDate.value,
            "accountId": accountId,
            'type': 'accounting_period',
            "fiscalYear": fiscalYear
        }),
    }).then((res) =>{
        console.log(res)
        window.location.reload();
    })
}

const handleFiscalYearClick = e => {
    fiscalYear = e.target.textContent;

    // TODO - make this into a GET request
    let url = '/advertising/ajax/finance/get_accounting_periods';
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "fiscalYear": fiscalYear,
            "accountId": accountId
        }),
    })
    .then((res) => res.json())
    .then(data => populateAPTable(data));
}

for (let i = 0; i < fiscalYearsTbody.rows.length; i++) {
    let row = fiscalYearsTbody.rows[i];
    let cells = row.cells;

    let nameCell = cells[0];
    nameCell.addEventListener('click', handleFiscalYearClick)
}

const handleActionBtnClick = e => {
    let dataset = e.target.parentElement.dataset;
    let status = dataset.status;
    let accountingPeriodId = dataset.accountingPeriod;
    console.log(status, accountingPeriodId);

    let url = `/advertising/ajax/finance/accounting-period/${accountingPeriodId}/action/`;

    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "status": status,
        }),
    })
    .then((res) => res.json())
    .then(res => {
        console.log(res);
        window.location.reload();
    })
    .catch(err => console.error(err))
}

const populateAPTable = data => {
    let rows = data.accountingPeriods;
    let tableRows = accountingPeriodTbody.rows;
    
    while(tableRows.length > 0) {
        accountingPeriodTbody.deleteRow(0);
    }

    rows.forEach(row => {
        let newRow = accountingPeriodTbody.insertRow();
        newRow.innerHTML += `<tr data-accounting-period="${row.id}">
                        <td>${row.code}</td>
                        <td>${row.period}</td>
                        <td>${row.start_date}</td>
                        <td>${row.end_date}</td>
                        ${row.status ? 
                            `<td style="color: green">Open</td>` : 
                            `<td style="color: red">Closed</td>`
                        }
                        <td data-status="${row.status}" data-accounting-period="${row.id}">
                            ${row.status ? 
                                `<button class="btn btn-default btn-sm action-btn">Close</button>` : 
                                `<button class="btn btn-default btn-sm action-btn">Open</button>`
                            }
                        </td>
                        <td><button class="btn btn-default btn-sm view-invoice">View Invoices</button></td>
                    </tr>`;
    });

    const actionBtns = document.querySelectorAll('.action-btn');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', handleActionBtnClick);
    });

    viewInvoiceBtns = [...document.querySelectorAll('.view-invoice')];
    viewInvoiceBtns.forEach(btn => btn.addEventListener('click', handleViewInvoices));
}

const handleViewInvoices = e => {
    $('#view_invoices_modal').modal('show');
    let row = e.target.parentElement.parentElement;
    let rowArray = row.getElementsByTagName('td');
    let rowDataset = rowArray[5].dataset;
    let periodId = rowDataset.accountingPeriod;

    fetch(`/advertising/ajax/accounting_period/invoices/?periodId=${periodId}&accountId=${accountId}`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        let invoiceData = data.invoices;
        if (invoiceData.length > 0) {
            let rows = '';
            for (let i = 0; i < invoiceData.length; i++) {
                let invoice = invoiceData[i];
                rows += `<tr>
                            <td>${new Date(invoice.date_sent).toLocaleString('en-US')}</td>
                            <td>${invoice.amount}</td>
                            <td>${invoice.bill_end}</td>
                            ${invoice.is_paid ? "<td><i class='fa fa-check'></i></td>" : "<td></td>"}
                            ${invoice.is_paid ? `<td>${new Date(invoice.date_paid).toLocaleString('en-US')}</td>` : "<td></td>"}
                        </tr>`;
            }
            $('#view_invoices_table tbody').append(rows);
        } else {
            let rows = '';
            rows += '<tr><td colspan="6">No Invoices</td></tr>'
            $('#view_invoices_table tbody').append(rows);
        }
    });
}

$('#view_invoices_modal').on('hide.bs.modal', e => $('#view_invoices_table tbody').empty());

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}

calendarYearToggle.addEventListener('input', handleCalendarYearToggle);
fiscalYearsSubmitBtn.addEventListener('click', handleFiscalYearsSubmit);
accountPeriodSubmitBtn.addEventListener('click', handleAccountingPeriodSubmit);