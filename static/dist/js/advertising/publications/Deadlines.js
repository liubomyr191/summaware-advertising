const deadlinesTable = document.querySelector('#adDeadlinesTable');

const addPubDaySelect = document.querySelector('#add_publication_day');
const addTimeInput = document.querySelector('#add_deadline_time');
const addAdTypeSelect = document.querySelector('#deadline_ad_type');
const addDaysPrior = document.querySelector('#deadline_days_prior');
const addPriorityLevelSelect = document.querySelector('#deadline_priority');

const addDeadlineSubmit = document.querySelector('#add_deadline_submit');

const editPubDaySelect = document.querySelector('#edit_publication_day');
const editTimeInput = document.querySelector('#edit_time');
const editAdTypeSelect = document.querySelector('#edit_ad_type');
const editDaysPrior = document.querySelector('#edit_days_prior');
const editPriorityLevelSelect = document.querySelector('#edit_priority');

const editDeadlineBtns = document.querySelectorAll('.edit-deadline');

const editDeadlineSubmit = document.querySelector('#edit_deadlines_submit');

let deadlineId;

$('#add_deadline_modal').on('show.bs.modal', function (e) {
    fetch(`/advertising/publication/${publication_id}/run-days/`, {
        method: "GET"
    })
        .then(res => {
            if (!res.ok) {
                alert(res.statusText);
            } else {
                return res.json();
            }
        })
        .then(data => {
            console.log(data);

            if (data.run_days) {
                for (let day of data.run_days) {
                    $('#add_publication_day').append(`<option value="${day}">${title(day)}</option>`);
                }
            }
        });
})

editDeadlineBtns.forEach(btn => btn.addEventListener('click', function (e) {
    deadlineId = e.target.parentElement.dataset.deadlineId;
    $('#edit_deadline_modal').modal('show');
}));

$('#edit_deadline_modal').on('show.bs.modal', function (e) {
    if (deadlineId) {
        fetch(`/advertising/publication/${publication_id}/deadlines/${deadlineId}/`, {
            method: "GET"
        })
            .then(res => {
                if (!res.ok) {
                    alert(res.statusText);
                } else {
                    return res.json();
                }
            })
            .then(data => {
                let deadline = data.deadline;

                if (data.runDayList) {
                    let runDayList = data.runDayList;

                    for (let [key, value] of Object.entries(runDayList)) {
                        if (daysOfTheWeek.includes(key) && runDayList[key]) {
                            $('#edit_publication_day').append(`<option value="${key}">${title(key)}</option>`);
                        }
                    }
                }

                selectOption(editPubDaySelect, (deadline.publication_day).toLowerCase());
                editTimeInput.value = deadline.time;
                selectOption(editAdTypeSelect, deadline.ad_type);
                editDaysPrior.value = deadline.days_prior;
                selectOption(editPriorityLevelSelect, deadline.priority_level);
            })
    }
});

$('#edit_deadline_modal').on('show.bs.modal', function (e) {
    $('#edit_publication_day').empty();
});

editDeadlineSubmit.addEventListener('click', function (e) {
    e.preventDefault();

    fetch(`/advertising/publication/${publication_id}/deadlines/${deadlineId}/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            publication_day: getSelectedOption(editPubDaySelect),
            time: editTimeInput.value,
            ad_type: getSelectedOption(editAdTypeSelect),
            days_prior: editDaysPrior.value,
            priority_level: getSelectedOption(editPriorityLevelSelect)
        })
    })
        .then(res => {
            if (!res.ok) {
                alert(res.statusText);
            } else {
                return res.json();
            }
        })
        .then(data => {
            console.log(data)

            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#edit_deadline_modal').modal('hide');
                window.location.reload();
            }
        })
});