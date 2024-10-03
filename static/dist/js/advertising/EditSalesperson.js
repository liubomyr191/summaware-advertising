console.log('EditSalesperson.js');

var salesperson_id = "{{ salesperson.id }}";
var submitBtn = document.getElementById("edit-details-btn");

var salespersonId = "{{ salesperson.id }}";
var editSalespersonForm = document.getElementById("edit-salesperson-form");

submitBtn.addEventListener("click", function (event) {
    document.getElementById("edit-salesperson-form").submit();

    const data = new FormData(editSalespersonForm);
    const formValues = {};
    for (let [name, value] of data) {
        formValues[name] = value;
    }
    formValues['active'] = formValues['active'] === 'on' ? true : false;

    $.ajax({
        type: 'POST',
        data: formValues,
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            console.log(data);
            alert('An error occurred while updating the salesperson.');
        }
    });
})
