let daysoftheWeek = {
    'sunday': 'Sunday',
    'monday': 'Monday',
    'tuesday': 'Tuesday',
    'wednesday': 'Wednesday',
    'thursday': 'Thursday',
    'friday': 'Friday',
    'saturday': 'Saturday'
};

$(document).ready(function () {
    let deadline = JSON.parse(deadlineJSON.replace(/'/g, '"'));
    console.log(deadline);
    $.ajax({
        url: `/advertising/ajax/publication/${publication_id}/run-days/`,
        type: 'GET',
        success: function (data) {
            let runDays = data.results;
            console.log(runDays)
            // loop through the results and add to the dropdown 
            for (let i = 0; i < runDays.length; i++) {
                let runDay = runDays[i];
                for (let [key, value] of Object.entries(runDay)) {
                    if (daysoftheWeek[key] !== undefined) {
                        if (runDay[key]) {
                            $('#publication_day').append(`<option value="${key}">${daysoftheWeek[key]}</option>`);
                            if (daysoftheWeek[key] == deadline.publication_day) {
                                $('#publication_day').find(`option[value="${key}"]`).attr('selected', true);
                            }
                        }
                    }
                }
            };
        },
        error: function (data) {
            console.log(data);
        }
    });
});