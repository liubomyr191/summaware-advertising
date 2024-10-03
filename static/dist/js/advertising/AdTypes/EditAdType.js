const editLinks = document.querySelectorAll('.edit-ad-type-link');

var adTypeTable = document.getElementById('ad_types_table');
var adTypeTableBody = adTypeTable.getElementsByTagName('tbody')[0];

var rowId;

editLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const id = link.getAttribute('data-type-id');

        var rows = adTypeTableBody.getElementsByTagName('tr');
        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            rowId = row.getElementsByTagName('td')[0].innerText;
            if (rowId == id) {
                var name = row.getElementsByTagName('td')[1].innerText;
                var code = row.getElementsByTagName('td')[2].innerText;
                break;
            }
        }

        var form = document.getElementById('edit-ad-type-form');
        form.elements.namedItem('name').value = name;
        form.elements.namedItem('code').value = code;
    });
});

document.getElementById('edit-ad-type-submit-btn').addEventListener('click', function (event) {
    const data = new FormData(document.getElementById('edit-ad-type-form'));
    const formValues = {};
    for (let [name, value] of data) {
        formValues[name] = value;
    }
    formValues['id'] = rowId;

    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        },
        data: {
            "type": "edit",
            "data": formValues
        },
        success: function (data) {
            location.reload();
        }
    });
});