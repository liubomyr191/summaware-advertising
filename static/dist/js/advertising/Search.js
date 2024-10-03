const searchInput = document.querySelector('#search-input');

const publicationTable = document.querySelector('#publication-table');
const publicationTableBody = publicationTable.querySelector('tbody');
const publicationTableRows = publicationTableBody.querySelectorAll('tr');

const accountTable = document.querySelector('#account-table');
const accountTableBody = accountTable.querySelector('tbody');
const accountTableRows = accountTableBody.querySelectorAll('tr');



searchInput.addEventListener('keyup', () => {
    const searchValue = searchInput.value;

    searchPublication(searchValue);
    searchAccount(searchValue);
});

const searchPublication = (searchValue) => {
    publicationTableRows.forEach(row => {
        const rowTitle = row.querySelector('td:nth-child(2)').innerText;

        if (searchValue === "") {
            row.style.display = '';
        } else if (!rowTitle.toLowerCase().includes(searchValue.toLowerCase()))
            row.style.display = 'none';
    });
};

const searchAccount = (searchValue) => {
    accountTableRows.forEach(row => {
        const rowTitle = row.querySelector('td:nth-child(2)').innerText;

        if (searchValue === "") {
            row.style.display = '';
        } else if (!rowTitle.toLowerCase().includes(searchValue.toLowerCase()))
            row.style.display = 'none';
    });
};

// document.body.addEventListener('keyup', (event) => {
//     if (event.target.id === 'adsearch-input') {
//       const searchValue = event.target.value;
//       console.log(searchValue);
//     }
// });
