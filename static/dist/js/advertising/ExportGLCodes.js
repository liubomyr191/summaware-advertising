var codesTable = document.getElementById('glCodesTable');
var codesTableBody = codesTable.getElementsByTagName('tbody')[0];
var codesTableRows = codesTableBody.getElementsByTagName('tr');
var codesTableRowCount = codesTableRows.length;

var codes = [];

for (var i = 0; i < codesTableRowCount; i++) {
    var codesTableRow = codesTableRows[i];
    var codesTableRowCells = codesTableRow.getElementsByTagName('td');

    var code = {
        code: codesTableRowCells[1].innerText,
        description: codesTableRowCells[2].innerText,
    }

    codes.push(code);
}

var exportBtn = document.getElementById('exportCodesBtn');
exportBtn.addEventListener('click', function () {
    var csvContent = "data:text/csv;charset=utf-8,";
    codes.forEach(function (code) {
        csvContent += code.code + ',' + code.description + "\n";
    });

    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "gl_codes.csv");
    document.body.appendChild(link);

    link.click();
});