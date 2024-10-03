var hasAdjustments = false;

var ratePrice = 0;
var adjustmentPrice = 0;
var finalPrice = 0;
var rateDetails;
var sales_person_name = "";

var selectedRates = {};
var numberUnitPrices = {};

let creditLimit;
let needsManagerOverride;

var colorTypes = {
    "full_color": "Full Color",
    "black_and_white": "Black and White",
    "solid_color": "Solid Color"
}

var sizes = {
    "quarter": "Quarter Page",
    "half": "Half Page",
    "full": "Full Page"
}

$('#subtotalModal').on('show.bs.modal', function (event) {
    checkForAdjustments();

    var subtotalTable = document.getElementById('subtotal-table');
    var subtotalTableBody = subtotalTable.getElementsByTagName('tbody')[0];

    var formData = $('#new_order_form').serializeArray();

    let publicationRateSelects = document.querySelectorAll('.publication-rate-select');
    for (let i = 0; i < publicationRateSelects.length; i++) {
        let options = publicationRateSelects[i].options;
        for (let j = 0; j < options.length; j++) {
            if (options[j].selected) {
                let pubId = publicationRateSelects[i].name.split('-')[1];
                selectedRates[pubId] = {
                    'rate_id': options[j].value
                }
            }
        }
    }

    let numberUnitInputs = document.querySelectorAll('.number-units');
    for (let i = 0; i < numberUnitInputs.length; i++) {
        let pubId = numberUnitInputs[i].name.split('-')[1];
        let inputValue = numberUnitInputs[i].value;
        selectedRates[pubId]['number_units'] = inputValue;
    }

    let subtotalData = {};

    let adjustments = [];
    let publications = [];
    formData.forEach(function (item) {
        if (item.name === 'publication') {
            publications.push(item.value);
        } else if (item.name == 'ad_type' || item.name == 'ad_rate') {
            return;
        } else if (item.name.startsWith('adjustment')) {
            adjustments.push(item.name);
        } else {
            subtotalData[item.name] = item.value;
        }
    });

    var getData = $.ajax({
        type: "POST",
        url: 'http://localhost:8000/advertising/ajax/order/subtotal/',
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        },
        data: JSON.stringify({
            "accountId": $('#account').val(),
            'ad_type': $('#ad_type').val(),
            'ad_rate': selectedRates,
            'publications': publications,
            'adjustments': adjustments,
            'salesperson': $('#sales_person').val(),
            "start_date": $('#start_date').val(),
            "end_date": $('#end_date').val()
        }),
        success: (result) => {

            creditLimit = result['creditLimit']

            subtotalData['publications'] = result['publications'].join(', ');

            rateDetails = result['ad_rates'];
            for (let [key, value] of Object.entries(rateDetails)) {
                finalPrice += Number(value.subtotal);
                subtotalData[key + ' rate'] = value.rate_details.name;
            }
            subtotalData['Ad Type'] = result['ad_type'].name;

            sales_person_name = result['sales_person'].first_name + ' ' + result['sales_person'].last_name;
            adjustmentsData = result['adjustments'];

            $('#totalInsertions').text(result.totalInsertions);

            let entries = Object.entries(result.insertion_list)
            for (let i = 0; i < entries.length; i++) {
                let publicationName = entries[i][0];
                let runDays = entries[i][1];
                let numInsertions = entries[i][1].length;

                let insertionDiv = $(`<div class="panel panel-default insertion-details"></div>`);
                insertionDiv.append(`<div class="panel-heading">
                                        <h4 class="panel-title">
                                            <a data-toggle="collapse" data-parent="#insertion_list" href="#heading${i}">
                                            ${publicationName} - ${numInsertions}</a>
                                        </h4>
                                    </div>
                                    <div id="heading${i}" class="panel-collapse collapse">
                                        <div class="panel-body">
                                            <div id="publication${i}-insertions"></div>
                                        </div>
                                    </div>`);

                $('#insertion_list').append(insertionDiv);

                for (let j = 0; j < runDays.length; j++) {
                    $(`#publication${i}-insertions`).append(`<p>${runDays[j]['weekday']} - ${runDays[j]['date']}</p>`)
                }
            }
        },
        error: (result) => {
            console.log(result.statusText);
        }
    });

    getData.done(function () {
        let isCustomSize = false;
        let inColor = false;
        console.log(subtotalData);

        for (let [key, value] of Object.entries(subtotalData)) {
            if (key === 'csrfmiddlewaretoken') {
                subtotalData = removeKey(key, subtotalData);
            }

            if (key.startsWith('publication-')) {
                subtotalData = removeKey(key, subtotalData);
            }

            if (key.startsWith('pub-')) {
                subtotalData = removeKey(key, subtotalData);
            }

            if ((key === 'color') && (subtotalData[key] === 'on')) {
                subtotalData[key] = 'Yes';
                inColor = true;
            }

            if (!inColor && (key === 'color_type')) {
                subtotalData = removeKey(key, subtotalData)
            }

            if (inColor && (key === 'color_type')) {
                subtotalData[key] = colorTypes[subtotalData[key]];
            }

            if (key == 'sales_person') {
                subtotalData[key] = sales_person_name;
            }

            if ((key === 'tearsheets') && (subtotalData[key] === 'on')) {
                subtotalData[key] = 'Yes';
            }

            if (key == 'size') {
                subtotalData[key] = sizes[subtotalData[key]];
            }

            if (key == 'size' && subtotalData[key] == undefined) {
                isCustomSize = true;
            }

            if (key == 'size' && subtotalData[key] == undefined) {
                subtotalData[key] = 'Custom';
            }

            if (key == 'publication') {
                publications.push(subtotalData[key]);
            }

        }

        for (let [key, value] of Object.entries(subtotalData)) {
            if (!hasValue(key, subtotalData)) {
                continue;
            }

            if (key.includes('_')) {
                key = key.replaceAll('_', ' ');
            }

            var row = subtotalTableBody.insertRow(subtotalTableBody.rows.length);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);

            cell1.innerHTML = capitalize(key);
            cell2.innerHTML = value;
        }

        if (hasAdjustments) {
            for (var i = 0; i < adjustmentsData.length; i++) {
                var row = subtotalAdjustmentsTableBody.insertRow(i);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);

                cell1.innerHTML = capitalize(adjustmentsData[i].code);
                cell2.innerHTML = "$" + adjustmentsData[i].price;

                adjustmentPrice += adjustmentsData[i].price;
            }
        } else {
            $('#subtotal-adjustments-table').hide();
        }

        if ($('#override_ad_cost').val() != "") {
            finalPrice = parseFloat($('#override_ad_cost').val());
        } 

        $('#finalPrice').text('$' + finalPrice);

        console.log(creditLimit, parseFloat(finalPrice), creditLimit < parseFloat(finalPrice));
    });
    account_id = $('#account').val();

    if ($('#save-draft').length) {
        $('#save-draft').on('click', (e) => {
            console.log(JSON.stringify($('#new_order_form').serializeArray()));

            $.ajax({
                type: "POST",
                url: '/advertising/order/new/',
                headers: {
                    "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
                },
                data: {
                    "formData": JSON.stringify($('#new_order_form').serializeArray()),
                    "is_draft": true,
                    "finalPrice": parseFloat(finalPrice),
                    "needs_manager_override": needsManagerOverride
                },
                success: (result) => {
                    window.location.href = '/advertising/account/' + $('#account').val() + '/drafts';
                }
            })
        });
    }
});

$('#subtotalModal').on('hide.bs.modal', function (event) {
    var subtotalTable = document.getElementById('subtotal-table');
    var subtotalTableBody = subtotalTable.getElementsByTagName('tbody')[0];
    var rowCount = subtotalTableBody.rows.length;
    for (var i = 0; i < rowCount; i++) {
        subtotalTableBody.deleteRow(0);
    }

    if (hasAdjustments) {
        var subtotalAdjustmentsTable = document.getElementById('subtotal-adjustments-table');
        if (subtotalAdjustmentsTable) {
            var subtotalAdjustmentsTableBody = subtotalAdjustmentsTable.getElementsByTagName('tbody')[0];
            var rowCount = subtotalAdjustmentsTableBody.rows.length;
            for (var i = 0; i < rowCount; i++) {
                subtotalAdjustmentsTableBody.deleteRow(0);
            }
        }
    }
    finalPrice = 0;
    ratePrice = 0;
    adjustmentPrice = 0;

    $('#insertion_list').empty();
});

if ($('#order-submit-btn').length) {
    document.getElementById('order-submit-btn').addEventListener('click', function (e) {
        e.preventDefault();

        let url = $('#new_order_form').attr('action');
        let formData = JSON.stringify($('#new_order_form').serializeArray());

        if (creditLimit < parseFloat(finalPrice)) {
            alert('Order Price is over the credit limit. Needs manager override');
            needsManagerOverride = true;
            $('#save-draft').trigger('click')

        } else {
            $.ajax({
                type: "POST",
                url: url,
                headers: {
                    "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
                },
                data: {
                    formData: formData,
                    finalPrice: parseFloat(finalPrice),
                },
                success: (result) => {
                    $("#subtotalModal").modal('hide');
                    window.location.href = `http://localhost:8000/advertising/account/${account_id}/`;
                },
                error: (result) => {
                    console.log('failure');
                    console.error(result.statusText);
                }
            });
        }
    });
};

const checkForAdjustments = () => {
    var adjustmentTableBody = $('#adjustment-table tbody');
    var adjustmentTableRowCount = $('#adjustment-table tbody tr');
    if (adjustmentTableRowCount) {
        $('#adjustment-table [type="checkbox"]').each(function (i, chk) {
            if (chk.checked) {
                hasAdjustments = true;
                console.log("Checked!", chk.value, chk.name);
            }
        });
    }

    if (!adjustmentTableRowCount) {
        $('#subtotal-adjustments-table').hide();
    } else {
        hasAdjustments = true;
        var subtotalAdjustmentsTable = document.getElementById('subtotal-adjustments-table');
    }
}

const capitalize = string => {
    const words = string.split(" ");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }
    return words.join(" ");
}

const hasValue = (key, object) => {
    return object[key] != '' && object[key] != null && object[key] != undefined && object[key] != 0;
}

const removeKey = (key, { [key]: _, ...rest }) => rest;