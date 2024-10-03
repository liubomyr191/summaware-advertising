const deadlinesTable = document.querySelector('#new_deadlines_table');
const deadlinesSubmitBtn = document.querySelector('#new_deadlines_submit');

const runDaysSelect = document.querySelector('#runDays');

const pubDaySelect = document.querySelector('#publication_day');
const timeInput = document.querySelector('#time');
const adTypeSelect = document.querySelector('#ad_type');
const daysPriorInput = document.querySelector('#days_prior');

const newPubSubmitBtn = document.querySelector('#new_pub_submit_btn');

let adDeadlines = [];

$('#add_deadline_modal').on('show.bs.modal', function (e) {
    for (const day of getSelectedOptions(runDaysSelect)) {
        $('#publication_day').append(`<option value="${day}">${title(day)}</option>`);
    }
});

$('#add_deadline_modal').on('hide.bs.modal', function (e) {
    $('#publication_day').empty();
    updateTable();
});

deadlinesSubmitBtn.addEventListener('click', function (e) {
    e.preventDefault();

    let selectedAdType = {}
    for (let i = 0; i < adTypeSelect.options.length; i++) {
        let option = adTypeSelect.options[i];
        if (option.selected)
            selectedAdType = { name: option.textContent, value: option.value }
    }

    for (let day of getSelectedOptions(pubDaySelect)) {
        adDeadlines.push({
            name: 'deadline',
            publication_day: title(day),
            time: timeInput.value,
            ad_type: selectedAdType,
            days_prior: daysPriorInput.value
        })
    }

    $('#add_deadline_modal').modal('hide');
    updateTable();
});

function updateTable() {
    $('#new_deadlines_table tbody').empty();

    for (const object of adDeadlines) {
        $('#new_deadlines_table tbody').append(`<tr>
                                                    <td>${object['publication_day']}</td>
                                                    <td>${object['time']}</td>
                                                    <td>${object['ad_type']['name']}</td>
                                                    <td>${object['days_prior']}</td>
                                                    <td>
                                                        <button type="button" class="btn btn-xs btn-default remove-deadline-btn">Remove</button>
                                                    </td>
                                                </tr>`);
    }
};

newPubSubmitBtn.addEventListener('click', function (e) {
    console.log(adDeadlines)
    let formDataObj = {};
    $('#new_pub_form').serializeArray().forEach((value, key) => {
        if (!Reflect.has(formDataObj, key)) {
            formDataObj[key] = value;
            return;
        }
        if (!Array.isArray(formDataObj[key])) {
            formDataObj[key] = [formDataObj[key]];
        }
        formDataObj[key].push(value);
    });
    let formDataJSON = JSON.stringify(formDataObj);

    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    formData.append('formData', formDataJSON);
    formData.append('deadlines[]', JSON.stringify(adDeadlines))

    $.ajax({
        type: 'POST',
        url: `/advertising/publication/new/`,
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        success: function (data) {
            console.log(data);
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else if (data.pubId) {
                window.location.href = `/advertising/publication/${data.pubId}`;
            } else {
                alert('Sorry, there was an error creating the publication. Please try again.');
                return;
            }
        },
        error: function (xhr, errmsg, err) {
            console.error(errmsg);
            return;
        }
    });
})