console.log('OrderDrafts.js');

var url = $('#new_order_form').attr('action');

$(document).ready(function() {
    // TODO - When the page loads, the rate is not selected
    if ($('#publication').val() && $('#ad_type').val()) {
        $.ajax({
            type: "GET",
            url: 'http://localhost:8000/advertising/ajax/order/search/rates/',
            data: {
                'publications[]': $('#publication').val(),
                ad_type: $('#ad_type').val()
            },
            success: (result) => {
                console.log(result)
                $('#ad_rate').empty();
                $('#ad_rate').append('<option value="">Select Ad Rate</option>');
                result['rates'].forEach(function (item) {
                    // console.log(item.id, parseInt(draftAdRateId))
                    // TODO - move this validation to the back end 
                    // if (item.start_date <= today && item.end_date >= today) {
                    $('#ad_rate').append('<option value="' + item.id + '">' + item.name + '</option>');
                    // }
                    // if (item.id == parseInt(draftAdRateId)) {
                    //     $('#ad_rate').val(draftAdRateId);
                    // }
                });
            },
            error: (result) => {
                alert(result.statusText);
            }
        });
    }
});

$('#save-edited-draft').on('click', (e) => {
    console.log(JSON.stringify($('#new_order_form').serializeArray()));

    $.ajax({
        type: "POST",
        url: url,
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        },
        data: {
            "order_number": draftId,
            "formData": JSON.stringify($('#new_order_form').serializeArray()),
            "is_draft": true,
            "finalPrice": parseFloat(finalPrice)
        },
        success: (result) => {
            window.location.href = '/advertising/account/' + $('#account').val() + '/drafts';
        }
    })
});

document.getElementById('draft-submit-btn').addEventListener('click', function (e) {
    e.preventDefault();
    var formData = JSON.stringify($('#new_order_form').serializeArray());
    $.ajax({
        type: "POST",
        url: url,
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        },
        data: {
            "order_number": draftId,
            "is_draft": false,
            formData: formData,
            finalPrice: parseFloat(finalPrice),
        },
        success: (result) => {
            $("#subtotalModal").modal('hide');
            window.location.href = `http://localhost:8000/advertising/account/${account_id}/orders/`;
        },
        error: (result) => {
            console.log('failure');
            console.error(result.statusText);
        }
    });
});