const searchInput = document.getElementById('ad-type-search-input');

var adTypeTable = document.getElementById('ad_types_table');
var adTypeTableBody = adTypeTable.getElementsByTagName('tbody')[0];
var tbodyRows = adTypeTableBody.getElementsByTagName('tr');

searchInput.addEventListener('keyup', () => {
    let searchString = searchInput.value.toLowerCase();
    for (let i = 0; i < tbodyRows.length; i++) {
        let row = tbodyRows[i];
        let rowText = row.innerText.toLowerCase();
        if (rowText.includes(searchString)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
});

const searchTable = (filter, term) => {
    let rows = tbodyRows;
    let filtered = [];
    for (let i = 0; i < rows.length; i++) {
        let row = rows[i];
        let rowText = row.innerText;
        if (rowText.toLowerCase().indexOf(term.toLowerCase()) > -1) {
            filtered.push(row);
        }
    }
    if (filter === '') {
        for (let i = 0; i < filtered.length; i++) {
            filtered[i].style.display = '';
        }
    } else {
        for (let i = 0; i < filtered.length; i++) {
            let rowText = filtered[i].innerText;
            if (rowText.toLowerCase().indexOf(filter.toLowerCase()) > -1) {
                filtered[i].style.display = '';
            } else {
                filtered[i].style.display = 'none';
            }
        }
    }
};