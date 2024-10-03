console.log('SalespersonShortcuts.js');

var salespersonTable = document.getElementById('shortcuts-table');
var salespersonTableBody = salespersonTable.getElementsByTagName('tbody')[0];
var salespersonTableRows = salespersonTableBody.getElementsByTagName('tr');

var actionDropdowns = document.querySelectorAll('#action-dropdown');

// get the dropdown for each row
for (var i = 0; i < salespersonTableRows.length; i++) {
    var dropdown = actionDropdowns[i];
    dropdown.addEventListener('change', function(e) {
        var selectedValue = e.target.value; // create_rate, create_rate, etc.

        var selectedRow = e.target.parentElement.parentElement;
        var rowAccountId = selectedRow.getAttribute('data-id');

        switch(selectedValue) {
            case 'create_order':
                window.location.href = 'order/new/' + rowAccountId;
                break;
            case 'create_rate':
                window.location.href = 'rate/new/';
                break;
            default:
                break;
        }
    });
}
