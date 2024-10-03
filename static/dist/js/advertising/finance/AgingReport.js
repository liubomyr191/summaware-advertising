let agingTable = document.querySelector('#aging_table');

let agingTableHeader = agingTable.getElementsByTagName('thead')[0];
let headerRow = agingTableHeader.getElementsByTagName('tr');
let headerCells = [...document.getElementsByTagName('th')];

let agingTableBody = agingTable.getElementsByTagName('tbody')[0];
let agingTableRows = [...agingTableBody.getElementsByTagName('tr')];

let agingReportFilters = headerCells.slice(5);

let filterDict = {
    "< 30 Days": "less_than_30",
    "31 - 60 Days": "31_60",
    "61 - 90 Days": "61_90",
    "90+ Days": "more_than_90"
}

let currDirection = 1;

const handleFilterClick = e => {
    let index = e.target.cellIndex;
    let newRows = Array.from(agingTableRows);

    newRows.sort(function (rowA, rowB) {
        let cellA = rowA.querySelectorAll('td')[index].textContent;
        let cellB = rowB.querySelectorAll('td')[index].textContent;

        // cellA = Number(cellA.split(' ')[1]) == 'NaN' ? 0 : Number(cellA.split(' ')[1]);
        // cellB = Number(cellB.split(' ')[1]) == 'NaN' ? 0 : Number(cellB.split(' ')[1]);

        switch (true) {
            case cellA > cellB: return 1 * currDirection;
            case cellA < cellB: return -1 * currDirection;
            case cellA === cellB: return 0;
        }
    });

    currDirection = currDirection === 1 ? -1 : 1;

    agingTableRows.forEach(row => agingTableBody.removeChild(row));
    newRows.forEach(row => agingTableBody.appendChild(row))
}

agingReportFilters.forEach(cell => cell.addEventListener('click', handleFilterClick));