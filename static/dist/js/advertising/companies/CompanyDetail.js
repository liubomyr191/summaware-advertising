const accountTable = document.querySelector('#account_table');
const accountTableBody = accountTable.getElementsByTagName('tbody')[0];

const searchInput = document.querySelector('#account_search');
const removeBtns = document.querySelectorAll('.remove-account-btn');

const currentCompanyCheckbox = document.querySelector('input[name="current-company"]');

let accountRows;
let companyAccountRows;

$('#add_account_modal').on('show.bs.modal', () => {
    fetch(`/advertising/ajax/company/accounts/?id=${company_id}`, {
        method: "GET",
    })
        .then(res => res.json())
        .then(data => {
            accountRows = data.accounts;
            companyAccountRows = data.company_accounts.map(account => account.account)

            populateTable(accountRows, companyAccountRows);
        })
        .catch(err => console.error(err))
});

$('#add_account_modal').on('hide.bs.modal', () => {
    $('#account_table tbody').empty();
    window.location.reload();
})

const populateTable = rows => {
    let tableRows = '';
    rows.forEach(row => {
        tableRows += `<tr>
                        <td>${row.id}</td>
                        <td>${row.name}</td>
                        <td>
                            <input type="checkbox" class="add-account-btn" value="${row.id}"/>
                        </td>
                        </tr>`;
    });
    $('#account_table > tbody').append(tableRows);

    searchInput.addEventListener('keyup', () => {
        [...accountTableBody.rows].forEach(row => {
            let name = row.getElementsByTagName('td')[1].textContent.toLowerCase();
            name.includes(searchInput.value) ? row.style.display = 'table-row' : row.style.display = 'none';
        })
    })

    let accountCheckboxes = [...document.querySelectorAll('.add-account-btn')];
    accountCheckboxes.forEach(box => {
        box.checked = companyAccountRows.includes(Number(box.value));

        box.addEventListener('click', (e) => {
            fetch('/advertising/ajax/company/accounts/', {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "Accept": "application/json",
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "account_id": e.target.value,
                    "company_id": company_id,
                    "checked": box.checked
                })
            })
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                })
                .catch(err => console.error(err))
        });
    });
};

if (removeBtns.length) {
    removeBtns.forEach(btn => {
        btn.addEventListener('click', e => {
            let row = e.target.parentElement.parentElement;
            let dataset = row.dataset;
            let accountId = dataset.account;

            let deleteConfirmation = confirm("Are you sure you want to remove this account?");
            if (deleteConfirmation) {
                fetch('', {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie('csrftoken'),
                        "Accept": "application/json",
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "account_id": accountId,
                    })
                })
                    .then(res => res.json())
                    .then(data => {
                        alert(data.message)
                        window.location.reload()
                    })
                    .catch(err => console.error(err))
            }
        })
    });
}

currentCompanyCheckbox.addEventListener('click', e => {
    let isChecked = e.target.checked;

    fetch('/advertising/company/current-company/', {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "companyId": company_id,
            "isChecked": isChecked

        })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data)
        })
        .catch(err => console.error(err))
});