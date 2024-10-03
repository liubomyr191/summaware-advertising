console.log('FilterDrafts.js');

$(document).ready(function() {
    const draftsTable = document.getElementById('drafts-table');
    const draftsTableBody = draftsTable.getElementsByTagName('tbody')[0];
    
    const draftInput = document.getElementById('draft-input');
    const draftSelect = document.getElementById('draft-select');

    const rowHeaders = draftsTable.getElementsByTagName('th');
    const rowHeadersNames = [];
    for (let i = 0; i < rowHeaders.length; i++) {
        if (rowHeaders[i].innerText.length > 0) {
            rowHeadersNames.push(toTitleCase(rowHeaders[i].innerText));
        }
    }

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.innerText = 'Select a column...';
    draftSelect.appendChild(defaultOption);
    for (let i = 0; i < rowHeadersNames.length; i++) {
        const option = document.createElement('option');
        option.value = rowHeadersNames[i];
        option.innerText = rowHeadersNames[i];
        draftSelect.appendChild(option);
    }
    draftInput.addEventListener('keyup', function() {
        const selectedOption = draftSelect.options[draftSelect.selectedIndex];
        const selectedOptionIndex = rowHeadersNames.indexOf(selectedOption.value);
        if (draftInput.value.length > 0) {
            for (let i = 0; i < draftsTableBody.rows.length; i++) {
                const row = draftsTableBody.rows[i];
                const cell = row.cells[selectedOptionIndex];
                if (cell.innerText.toLowerCase().indexOf(draftInput.value.toLowerCase()) === -1) {
                    row.style.display = 'none';
                } else {
                    row.style.display = '';
                }
            }
        } else {
            for (let i = 0; i < draftsTableBody.rows.length; i++) {
                const row = draftsTableBody.rows[i];
                row.style.display = '';
            }
        }
    });
});

function toTitleCase(str) {
    return str.replace( /\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}