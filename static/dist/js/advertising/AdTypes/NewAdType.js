const newAdTypesModal = document.getElementById('new-ad-type-modal');
const newAdTypeForm = document.getElementById('new-ad-type-form');
const newAdTypeSubmitBtn = document.getElementById('new-ad-type-submit-btn');

let newAdTypeName = document.querySelector('input[id="name"]');
let newAdTypeCode = document.querySelector('input[id="code"]');

newAdTypeSubmitBtn.addEventListener('click', function (event) {
    const data = new FormData(newAdTypeForm);
    const formValues = {};
    for (let [name, value] of data) {
        formValues[name] = value;
    }

    if (!newAdTypeName.value || !newAdTypeCode.value) {
        alert('Error. Please fill in both fields before submitting');
        return;
    }

    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        },
        data: {
            "type": "new",
            "data": formValues
        },
        success: function (data) {
            location.reload();
        }
    });
});