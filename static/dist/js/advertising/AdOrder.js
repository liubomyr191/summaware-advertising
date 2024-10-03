const selectAllPublications = document.querySelector('#select_all_publications');
const publicationSelect = document.querySelector('#publication');

var requiredFields = $('input,textarea,select').filter('[required]:visible')
var today = new Date().toISOString().split('T')[0];

var publicationValue;
var adTypeValue;
let days_prior;
let startDateValue
let late = false;
var orderDetails = {};

var showRateModal = false;

$(document).ready(function () {
    $('#account').on('change', getSalesPerson);
    $('#publication').on('change', handlePublicationChange);
    $('#publication').on('focusout', getAdjustments);

    $('#ad_type').on('change', e => adTypeValue = $(e.target).val());

    $('#ad_rate').change(getRateDetails);

    $('#select-rate-btn').on('click', e => {
        e.preventDefault();
        if (!(publicationValue && adTypeValue)) {
            alert('Select publications and an ad type before selecting the rates')
            return false;
        }
        $('.publication-rates').text('');

        $('#select-rate-modal').modal('show');

        let selectedPublications = document.querySelectorAll('#publication :checked');
        let publicationIds = [];
        let publicationList = '';

        for (let i = 0; i < selectedPublications.length; i++) {
            publicationList += `<div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="publication-${selectedPublications[i].value}-rates">
                                                ${selectedPublications[i].innerText}
                                            </label>
                                            <select class="form-control publication-rate-select" name="publication-${selectedPublications[i].value}-rates" 
                                                id="publication-${selectedPublications[i].value}-rates">
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="pub-${selectedPublications[i].value}-number-units">
                                                Number of Units
                                            </label>
                                            <input type="number" class="form-control number-units" id="pub-${selectedPublications[i].value}-number-units" name="pub-${selectedPublications[i].value}-number-units"/>
                                        </div>
                                    </div>
                                </div>`;
            publicationIds.push(selectedPublications[i].value)
        }
        $('.publication-rates').append(publicationList);


        let url = '/advertising/ajax/order/search/rates/';
        $.ajax({
            type: "GET",
            url: url,
            data: {
                "publications[]": publicationIds,
                "ad_type": adTypeValue
            },
            success: result => {
                var rates = result.rates ? result.rates : {};
                populateRates(rates);
            },
            error: error => {
                console.error(error.statusText)
            }
        });
    })

    var adjustments = [];
    $("#new_order_form").submit(function (e) {
        e.preventDefault();
        var adjustments = [];
        var adjustments_checkboxes = document.querySelectorAll('input[name=adjustment]:checked');
        for (var i = 0; i < adjustments_checkboxes.length; i++) {
            adjustments.push(adjustments_checkboxes[i].value);
        }
        confirmFormData = JSON.stringify($('#new_order_form').serializeArray());
    });

    // if bill_date is set to custom, show the custom_billing_date_form
    $('#bill_date').on('change', (e) => {
        if (e.target.value == 'custom') {
            $('#custom_billing_date_form').css("display", "block");
        } else {
            $('#custom_billing_date_form').css("display", "none");
        }
    })

    $('#submit-btn').on('click', (e) => {
        showMissingRequiredFields();
        if (isFormValid()) $('#subtotalModal').modal('show');
    });
});

selectAllPublications.addEventListener('click', e => {
    let checked = e.target.checked;

    for (let i = 0; i < publicationSelect.options.length; i++) {
        publicationSelect.options[i].selected = checked;
    }
});

const handlePublicationChange = e => {
    publicationValue = getSelectValues(publicationSelect)

    let colorTable = document.querySelector('#publication_color_table');
    let colorTableBody = colorTable.getElementsByTagName('tbody')[0];
    let publications = getSelectValuesDict(publicationSelect);
    
    $('#publication_color_table tbody').empty();

    publications.forEach((publication, index) => {
        let row = colorTableBody.insertRow(index);

        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        let cell4 = row.insertCell(2);

        cell1.innerHTML = publication.value;
        cell2.innerHTML = publication.name;
        cell4.innerHTML = `<select id="pub-${publication.value}-color-type" name="pub-${publication.value}-color-type">
                                <option value="">Select Color Type...</option>
                                <option value="full_color">Full Color</option>
                                <option value="black_and_white">Black and White</option>
                            </select>`;
    });

    getPublicationSpotColors();
}

const isFormValid = () => {
    var isValid = true;
    for (var i = 0; i < requiredFields.length; i++) {
        if (requiredFields[i].value == '') {
            isValid = false;
        }
    }
    return isValid;
}

const dateDifference = (first, second) => {
    return Math.floor((Date.parse(second) - Date.parse(first)) / 86400000);
}

const showMissingRequiredFields = () => {
    for (let i = 0; i < requiredFields.length; i++) {
        if (requiredFields[i].value == '') {
            requiredFields[i].style.border = '1px solid red';
        } else {
            requiredFields[i].style.border = '1px solid #ced4da';
        }
    }
}

const isEmptyObject = obj => Object.keys(obj).length === 0;

const getSalesPerson = () => {
    $.ajax({
        url: '/advertising/ajax/account/' + $('#account').val(),
        type: 'GET',
        success: (data) => {
            $('#sales_person').val(data.account.sales_person);
        }
    })
}

const getPublicationSpotColors = () => {
    $.ajax({
        url: '/advertising/publications/colors/',
        data: {
            "publications[]": getSelectValues(publication)
        },
        success: data => {
            populatePublicationDropdowns(data.colors);
        },
        failure: err => console.error(err)
    })
}

const populatePublicationDropdowns = colors => {
    $.each(colors, function (i, item) {
        $(`#pub-${item.publication_id}-color-type`).append($('<option>', { 
            value: item.color,
            text : `Solid Color: ${item.color}` 
        }));
    });
}

const getAdjustments = e => {
    let publications = $(e.target).val();
    $.ajax({
        url: '/advertising/ajax/publication/adjustments/',
        data: {
            "publications": publications
        },
        success: result => {
            let adjustments = result.adjustments ? result.adjustments : {};
            populateAdjustments(adjustments)
        }
    })
}

const getRates = () => {
    let url = 'http://localhost:8000/advertising/ajax/order/search/rates/'
    var rates = $.ajax({
        type: "GET",
        url: url,
        data: {
            'publications[]': publicationValue,
            ad_type: adTypeValue
        },
        success: (result) => {
            console.log(result)
            let publications = result.rates ? result.rates : [];
            let adRateOptions = '';
            for (let [name, rates] of Object.entries(publications)) {
                if (rates.length > 0) {
                    rates.forEach(rate => {
                        adRateOptions += `<option value=${rate.id}>${rate.name}</option>`
                    })
                }
            }
            $('#ad_rate').append(adRateOptions);
            $('#ad_rate').trigger('change');
        },
        error: (error) => {
            console.error(error)
            $('#ad_rate').append('<option value="">No rates found</option>');
            $('#rate-unit-type').text('');
            console.error(error.statusText);
        }
    });
}

const getRateDetails = (e) => {
    let url = 'http://localhost:8000/advertising/ajax/order/search/rate-details/';
    $.ajax({
        type: "GET",
        url: url,
        data: {
            ad_rate: $(e.target).val()
        },
        success: result => {
            let rate = result.rate;
            let unit = '';
            switch (rate.unit_type) {
                case 'word':
                    unit = 'word';
                    break;
                case 'line':
                    unit = 'line';
                    break;
                case 'column':
                    unit = 'column';
                    break;
                case 'inch':
                    unit = 'inch';
                    break;
            }
            $('#rate-unit-type').text(`$${rate.unit_price} per ${unit}`);
        },
        error: error => {
            if (error.status == 404 || error.status == 500) {
                $('#ad_rate').append('<option value="">No rates found</option>');
                $('#rate-unit-type').text('');
            }
        }
    });
};

const populateRates = rates => {
    console.log(rates)
    if (isEmptyObject(rates)) console.error('Codes provided are not an object');
    var rateSelects = document.querySelectorAll('.publication-rate-select');

    for ([key, value] of Object.entries(rates)) {
        rateSelects.forEach(rateSelect => {
            let publicationName = rateSelect.labels[0].textContent.trim();
            let publicationRates = value;

            if (publicationName == key) {
                if (publicationRates.length) {
                    for (var i = 0; i < publicationRates.length; i++) {
                        var option = document.createElement("option");
                        option.value = publicationRates[i].id;
                        option.text = `${publicationRates[i].name} - $${publicationRates[i].unit_price}/${publicationRates[i].unit_type}`;
                        rateSelect.appendChild(option);
                    }
                } else {
                    var option = document.createElement("option");
                    option.value = "";
                    option.text = 'No rates found';
                    option.selected = true;
                    option.disabled = true;
                    rateSelect.appendChild(option);
                }
            }
        })
    }
}

const populateAdjustments = adjustments => {
    if (isEmptyObject(adjustments)) console.error('The adjustments provided is an empty object');

    let adjustmentTableBody = $('#adjustment-table tbody');
    adjustmentTableBody.empty();

    for ([key, value] of Object.entries(adjustments)) {
        let publicationName = key;
        let adjustmentList = value;

        adjustmentList.forEach(adjustment => {
            let tableRow = '<tr>';
            tableRow += `<td>${publicationName}</td>
                            <td>${adjustment.code}</td>
                            <td>${adjustment.description}</td>
                            <td><input type="checkbox" class="form-check-input adjustment"
                                name="adjustment-${adjustment.id}" id="${adjustment.code}"></td>`;
            tableRow += '</tr>';
            adjustmentTableBody.append(tableRow);
        });
    };

    var adjustment_list = [];
    var adjustments = document.querySelectorAll('.adjustment');
    adjustments.forEach(adjustment => {
        adjustment.addEventListener('change', function (e) {
            if (e.target.checked) {
                console.log('checked')
                adjustment_list.push(e.target.id);
            } else {
                adjustment_list.splice(adjustment_list.indexOf(e.target.id), 1);
            }
        });
    });
}

const removeOptions = (element) => {
    var length = element.options.length;
    for (i = length - 1; i > 0; i--) {
        element.options[i] = null;
    }
}

const removeOption = (select, option) => {
    for (let i = 0; i < select.options.length; i++) {
        let currentOption = select.options[i];

        if (currentOption.value == option.value) {
            currentOption = null;
        }
    }
}

const getSelectValues = select => {
    var result = [];
    var options = select && select.options;
  
    for (let i=0; i < options.length; i++) {
      option = options[i];
  
      if (option.selected) {
        result.push(option.value || option.text);
      }
    }
    return result;
}

const getSelectValuesDict = select => {
    var result = [];
    var options = select && select.options;
  
    for (let i=0; i < options.length; i++) {
      option = options[i];
  
      if (option.selected) {
        result.push({
            "name": option.textContent,
            "value": option.value
        });
      }
    }
    return result;
}