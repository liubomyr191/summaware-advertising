const creditLimitTable = document.querySelector('#account_credit_table');
const creditLimtiTableBody = creditLimitTable.getElementsByTagName('tbody')[0];

const saveBtn = document.querySelector('#save_btn');

let tableRows = creditLimtiTableBody.getElementsByTagName('tr');
let accountCreditLimits = {};

const handleSave = e => {
    for (let i = 0; i < tableRows.length; i++) {
        let row = tableRows[i].children;
    
        let accountId = row[0].textContent;
        let creditLimit = row[2].children[0].value;
    
        if (!(accountId in accountCreditLimits)) {
            accountCreditLimits[accountId] = Number(creditLimit);
        }
    }
    
    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        data: { accountCreditLimits },
        success: function (data) {
            console.log(data)
            alert(data.message);
            window.location.reload();
        }
    });
}
if ($('#save_btn').length > 0) saveBtn.addEventListener('click', handleSave);

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}