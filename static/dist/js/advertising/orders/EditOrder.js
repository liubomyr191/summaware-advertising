const publicationBtns = document.querySelectorAll('.publication-button');
const publicationInputs = document.querySelectorAll('.publication-input');

const publicationDetailsSection = document.querySelector('#publicationDetails_column');

const billDateSelect = document.querySelector('#bill_date');
const customBillDate = document.querySelector('#custom_billing_date_form')

const dateInput = document.querySelector('#publication_dates');
const updateDatesBtn = document.querySelector('#update_dates');
const tfnCheckbox = document.querySelector('#till_further_notice');

const adTypeSelect = document.querySelector('#publication_adType');
const adRateSelect = document.querySelector('#publication_adRate');
const sizeSelect = document.querySelector('#size');

const numberUnitsGroup = document.querySelector('#numberUnitsGroup');
const numberUnitsLabel = document.querySelector('#numberUnitsLabel');
const numberUnitsInput = document.querySelector('#numberUnitsInput')

const adjustmentTable = document.querySelector('#publication_adjustmentTable');

const inColorCheckbox = document.querySelector('#color');
const colorTypeSelect = document.querySelector('#publication_colorType');

const priceLabel = document.querySelector('#price_label');
const priceValue = document.querySelector('#price_value');

const updateSummaryBtn = document.querySelector('#update_summary_btn');
const orderSaveBtn = document.querySelector('#order_save_btn');
const orderSubmitBtn = document.querySelector('#order-submit-btn');

let selectedPublications = [];
let selectedPublication = {};

let publicationOrderData = {};

let totalPrice = 0.00;

$(document).ready(() => {
    fetch(`/advertising/ajax/order/search/details/?orderId=${orderId}`, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            const orderPublications = data.order_publications;

            let orderPubList = [];

            orderPublications.forEach(result =>
                orderPubList.push(result.publication)
            )

            publicationBtns.forEach(button => {
                const checkboxInput = button.getElementsByTagName('input')[0]; // checkbox
                for (let i = 0; i < orderPubList.length; i++) {
                    if (orderPubList[i] == button.dataset.id) {
                        $(checkboxInput).trigger('click');
                        checkboxInput.checked = true;
                        $(button).trigger('click');

                        break;
                    }
                }
            })
            $('#update_summary_btn').trigger('click');
        });
});

const loadPublicationDetails = e => {
    let dataset = e.target.dataset;
    if (dataset.name == undefined || dataset.id == undefined) return;

    selectedPublication['id'] = dataset.id;
    selectedPublication['name'] = dataset.name;

    // TODO - refactor this to get all of the selectedPublications data at the start instead of making a request each time a publication is clicked 

    fetch(`/advertising/ajax/order/search/publication/?id=${selectedPublication.id}&orderId=${orderId}`, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            populateOptions(data);
        });
}

const populateOptions = data => {
    let rateList = data.rates;
    let adjustmentList = data.adjustments ? data.adjustments : [];
    let color = data.color;

    $('#publication_adRate').empty();
    for (let i = 0; i < selectedPublications.length; i++) {
        let currId = selectedPublications[i].split('-')[1];

        if (currId == selectedPublication.id) {
            let rateOptions = '';
            rateOptions += `<option value="">Select an ad rate ...</option>`
            for (let i = 0; i < rateList.length; i++) {
                let currRate = rateList[i];
                rateOptions += `<option value=${currRate.id}>${currRate.name} - $${currRate.price}/${currRate.unit_type}</option>`
            }
            $('#publication_adRate').append(rateOptions);

            break;
        } else {
            setDefaultValues();
        }
    }

    if (data.selectedData) {
        let selectedData = data.selectedData;


        publicationOrderData[selectedPublication.name]['dates']['label'] = "Dates";
        publicationOrderData[selectedPublication.name]['dates']['value'] = selectedData.dates;

        publicationOrderData[selectedPublication.name]['adRate']['value'] = selectedData.ad_rate.id;
        publicationOrderData[selectedPublication.name]['adRate']['label'] = "Ad Rate";

        publicationOrderData[selectedPublication.name]['adType']['name'] = selectedData.ad_type.name;
        publicationOrderData[selectedPublication.name]['adType']['value'] = selectedData.ad_type.code;
        publicationOrderData[selectedPublication.name]['adType']['label'] = "Ad Type";

        publicationOrderData[selectedPublication.name]['size']['name'] = "Size";
        publicationOrderData[selectedPublication.name]['size']['value'] = selectedData.size;
        publicationOrderData[selectedPublication.name]['size']['label'] = "Size";

        let rateValue = publicationOrderData[selectedPublication.name]['adRate']['value'];
        let typeValue = publicationOrderData[selectedPublication.name]['adType']['value'];
        let sizeValue = publicationOrderData[selectedPublication.name]['size']['value'];

        if (rateValue != undefined) selectOption(adRateSelect, rateValue);
        if (typeValue != undefined) selectOption(adTypeSelect, typeValue);
        if (sizeValue != undefined) selectOption(sizeSelect, sizeValue);

        publicationOrderData[selectedPublication.name]['adRate']['name'] = getSelectedOption(adRateSelect).name;

        numberUnitsGroup.style.display = getSelectedOption(adRateSelect).value == '' ? 'none' : 'block';
        let rateType = getSelectedOption(adRateSelect).name.split('/')[1];

        if (rateType == 'inch') {
            numberUnitsLabel.textContent = `${rateType}es`;
        } else {
            numberUnitsLabel.textContent = `${rateType}s`;
        }

        publicationOrderData[selectedPublication.name]['adRate']['units'] = {
            "label": numberUnitsLabel.textContent,
            "name": rateType,
        }
        publicationOrderData[selectedPublication.name]['adRate']['units']["value"] = selectedData.number_units;
        let numberUnitsValue = publicationOrderData[selectedPublication.name]['adRate']['units']["value"]
        numberUnitsInput.value = numberUnitsValue != '' ? numberUnitsValue : 0;

    } else {
        let rateValue = publicationOrderData[selectedPublication.name]['adRate']['value'];
        let typeValue = publicationOrderData[selectedPublication.name]['adType']['value'];
        let sizeValue = publicationOrderData[selectedPublication.name]['size']['value'];

        if (rateValue != undefined) selectOption(adRateSelect, rateValue);
        if (typeValue != undefined) selectOption(adTypeSelect, typeValue);
        if (sizeValue != undefined) selectOption(sizeSelect, sizeValue);

    }

    // $('#publication_dates').datepicker('refresh');
    if (publicationOrderData[selectedPublication.name]['dates']['value'] != '') {

        let previousDates = publicationOrderData[selectedPublication.name]['dates']['value'];
        if (previousDates != undefined) {
            // $("#publication_dates").multiDatesPicker('addDates', publicationOrderData[selectedPublication.name]['dates']['value']);
            $("#publication_dates").val(publicationOrderData[selectedPublication.name]['dates']['value']);
            dateInput.value = publicationOrderData[selectedPublication.name]['dates']['value'];
        } else {
            // console.log($("#publication_dates").multiDatesPicker('getDates'))
            $("#publication_dates").val('');
            dateInput.value = '';
        }
    }

    inColorCheckbox.checked = publicationOrderData[selectedPublication.name]['color'];
    if (inColorCheckbox.checked) {
        colorTypeSelect.style.display = 'block';
        selectOption(colorTypeSelect, publicationOrderData[selectedPublication.name]['colorType']);
    }

    $('#publication_adjustmentTable tbody').empty();

    let rows = '';
    if (adjustmentList.length == 0) {
        rows += '<tr><td colspan="4">No adjustments</td></tr>'
    } else {
        adjustmentList.forEach(adjustment => {
            rows += `<tr>
                    <td>${adjustment.code}</td>
                    <td>${adjustment.description}</td>
                    <td>$${adjustment.amount}</td>
                    <td><input class="adjustment-action" type="checkbox" data-id=${adjustment.id} /></td>
                </tr>`;
        });
    }
    $('#publication_adjustmentTable tbody').append(rows);

    let adjustmentActionBoxes = document.querySelectorAll('.adjustment-action');
    adjustmentActionBoxes.forEach(checkbox => checkbox.addEventListener('click', handleAdjustmentAction));

    if (adjustmentList.length) {
        let adjustmentsArray = publicationOrderData[selectedPublication.name]['adjustments'];
        adjustmentActionBoxes.forEach(checkbox => {
            if (adjustmentsArray.includes(checkbox.dataset.id)) checkbox.checked = true;
        });
    }
}

const handleAdjustmentAction = e => {
    let isChecked = e.target.checked;
    let adjustmentId = e.target.dataset.id;

    let adjustmentsArray = publicationOrderData[selectedPublication.name]['adjustments'];

    if (isChecked) {
        adjustmentsArray.push(adjustmentId);
    } else {
        let index = adjustmentsArray.indexOf(adjustmentId);
        if (index > -1) {
            adjustmentsArray.splice(index, 1);
        }
    }
    publicationOrderData[selectedPublication.name]['adjustments'] = adjustmentsArray;
}

const handlePublicationSelect = e => {
    let publicationName = e.target.dataset.name;

    if (e.target.checked) {
        selectedPublications.push(e.target.value);

        publicationOrderData[publicationName] = {};
        publicationOrderData[publicationName]['dates'] = {
            "label": "Dates"
        }
        publicationOrderData[publicationName]['adjustments'] = [];

        publicationOrderData[publicationName]['adRate'] = {
            "name": '',
            "value": ''
        }
        publicationOrderData[publicationName]['adType'] = {
            "name": '',
            "value": ''
        }
        publicationOrderData[publicationName]['size'] = {
            "name": '',
            "value": ''
        }
    } else {
        selectedPublications.pop(selectedPublications.length - 1);
        publicationOrderData = removeKey(publicationName, publicationOrderData);
    }

    if (selectedPublications.length == 1) {
        publicationDetailsSection.style.display = 'block';
    } else if (selectedPublications.length == 0) {
        setDefaultValues();
        publicationDetailsSection.style.display = 'none';
    }
}

const handleColorChange = e => {
    if (e.target.checked) {
        colorTypeSelect.style.display = 'block';
        publicationOrderData[selectedPublication.name]['color'] = true;

    } else {
        colorTypeSelect.style.display = 'none';
        publicationOrderData[selectedPublication.name]['color'] = false;
    }
}

const handleColorTypeChange = e => {
    let colorType = e.target.value;
    let inColor = publicationOrderData[selectedPublication.name]['color'];

    publicationOrderData[selectedPublication.name]['colorType'] = inColor ? colorType : '';
}

const handleDatesUpdate = e => {
    publicationOrderData[selectedPublication.name]['dates']['value'] = dateInput.value;
}

publicationBtns.forEach(btn => btn.addEventListener('click', loadPublicationDetails)) // Bootstrap list-group-items
publicationInputs.forEach(input => input.addEventListener('input', handlePublicationSelect)); // checkboxes 

inColorCheckbox.addEventListener('input', handleColorChange);
colorTypeSelect.addEventListener('change', handleColorTypeChange);

billDateSelect.addEventListener('change', e => customBillDate.style.display = e.target.value == 'custom' ? 'block' : 'none');

adTypeSelect.addEventListener('change', e => {
    publicationOrderData[selectedPublication.name]['adType'] = getSelectedOption(adTypeSelect);
    publicationOrderData[selectedPublication.name]['adType']['label'] = "Ad Type";
});

adRateSelect.addEventListener('change', e => {
    publicationOrderData[selectedPublication.name]['adRate'] = getSelectedOption(adRateSelect);
    publicationOrderData[selectedPublication.name]['adRate']['label'] = "Ad Rate";
    publicationOrderData[selectedPublication.name]['adRate']['name'] = getSelectedOption(adRateSelect).textContent;

    numberUnitsGroup.style.display = getSelectedOption(adRateSelect).value == '' ? 'none' : 'block';
    let rateType = getSelectedOption(adRateSelect).name.split('/')[1];

    if (rateType == 'inch') {
        numberUnitsLabel.textContent = `${rateType}es`;
    } else {
        numberUnitsLabel.textContent = `${rateType}s`;
    }

    publicationOrderData[selectedPublication.name]['adRate']['units'] = {
        "label": numberUnitsLabel.textContent,
        "name": rateType,
    }
});

numberUnitsInput.addEventListener('input', e => {
    publicationOrderData[selectedPublication.name]['adRate']['units']["value"] = e.target.value
})

sizeSelect.addEventListener('change', e => {
    publicationOrderData[selectedPublication.name]['size'] = getSelectedOption(sizeSelect);
    publicationOrderData[selectedPublication.name]['size']['label'] = "Size";
});

updateDatesBtn.addEventListener('click', handleDatesUpdate);

tfnCheckbox.addEventListener('click', e => {
    if (e.target.checked) {
        publicationOrderData[selectedPublication.name]['dates']['value'] = 'till_further_notice';
        publicationOrderData[selectedPublication.name]['dates']['name'] = 'Until Further Notice';

        dateInput.value = '';
        dateInput.disabled = true;
    } else {
        publicationOrderData[selectedPublication.name]['dates']['value'] = '';
        publicationOrderData[selectedPublication.name]['dates']['name'] = '';

        dateInput.disabled = false;
    }
});

$('#publication_dates').multiDatesPicker({
    multidate: true,
    format: "yyyy-mm-dd",
    defaultDate: null,
    minDate: 0
});

const removeOptions = (element) => {
    var length = element.options.length;
    for (i = length - 1; i > 0; i--) {
        element.options[i] = null;
    }
}

const selectOption = (select, value) => {
    if (value == undefined) return;
    for (let i = 0; i < select.options.length; i++) {
        let currOption = select.options[i];

        if (currOption.value == value) {
            currOption.selected = true;
            break;
        }
    }
}

const setDefaultOption = (select) => {
    for (let i = 0; i < select.options.length; i++) {
        let currentOption = select.options[i];

        if (currentOption.value == '') {
            currentOption.selected = true;
            break;
        }
    }
}

const setDefaultValues = () => {
    removeOptions(adRateSelect);
    setDefaultOption(adTypeSelect);
    setDefaultOption(sizeSelect);

    $("#publication_dates").val('');
    dateInput.value = '';
}

const removeKey = (property, obj) => {
    const { [property]: unused, ...rest } = obj;
    return rest;
}

const isEmpty = obj => Object.keys(obj).length === 0;

const getSelectedOption = select => {
    for (let i = 0; i < select.options.length; i++) {
        let option = select.options[i];
        if (option.selected) return { "name": option.text, "value": option.value }
    }
}

const getCookie = name => {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}

const title = word => {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

/*
---------------------------------------------------
    Order Summary Page
---------------------------------------------------
*/

const summaryLeftContent = document.querySelector('#summary_left_content');
const summaryRightContent = document.querySelector('#summary_right_content');

const subtotalRef = document.querySelector('#order_subtotal');
const totalRef = document.querySelector('#order_total');

let topLevelDetails;

updateSummaryBtn.addEventListener('click', evt => {
    evt.preventDefault();

    if (!selectedPublications.length) {
        alert('Please select publications first.');
        return;
    }

    $('#summary_left_content').empty();
    $('#summary_right_content').empty();

    topLevelDetails = {
        "Name": $('#name').val(),
        "Account": getSelectedOption(document.querySelector('#account'))['name'],
        "Ad Taker/Submitter": $('#adTaker').val(),
        "Salesperson": getSelectedOption(document.querySelector('#salesperson'))['name'],
        "Bill Date": getSelectedOption(document.querySelector('#bill_date'))['name'],
        "Invoice Frequency": getSelectedOption(document.querySelector('#invoiceFrequency'))['name'],
        "Notes": $('#notes').val(),
    };

    let hasCustomBillDate = getSelectedOption(document.querySelector('#bill_date'))['value'] == 'custom';
    let isTearsheet = document.querySelector('#tearsheets').checked;
    let hasOverrideAdCost = $('#overrideCost').val();

    if (hasCustomBillDate)
        topLevelDetails["Custom Bill Date"] = $('custom_billing_date').val();
    if (hasOverrideAdCost) {
        topLevelDetails["Override Ad Cost"] = `$${$('#overrideCost').val()}`;

        totalPrice = $('#overrideCost').val();
        totalRef.textContent = $('#overrideCost').val();
    }

    subtotalRef.textContent = `$${totalPrice}`;
    totalRef.textContent = `$${totalPrice}`;
    topLevelDetails['Total Price'] = totalPrice;

    topLevelDetails["Tearsheets"] = isTearsheet ? "Yes" : "No";

    for (const [key, value] of Object.entries(topLevelDetails)) {
        let row = '';
        row += `<div class="summary-content-row">
                    <div class="row-title">${key}</div>
                    <span class="dotted"></span>
                    <div class="row-value">${value}</div>
                </div>`;
        $('#summary_left_content').append(row);
    }

    for (const [pubName, pubData] of Object.entries(publicationOrderData)) {
        let row = `<button type="button" class="summary-accordion">${pubName}</button>`;
        row += `<div class="summary-panel">
                    <div class="summary-row summary-first-row">
                        <div>
                            <p class="section-name">Ad Type: </p>
                            <p>${pubData['adType']['name']}</p>
                        </div>
                        <div>
                            <p class="section-name">Ad Rate: </p>
                            <p>${pubData['adRate']['name']}</p>
                        </div>
                        <div>
                            <p class="section-name">Size: </p>
                            <p>${pubData['size']['name']}</p>
                        </div>
                    </div>
                    <div class="summary-row summary-third-row">
                        <div>
                            <p class="section-name">Run Dates: </p>
                            <p>${pubData['dates']['value']}</p>
                        </div>
                    </div>
                    <div class="summary-row summary-fourth-row">
                        <div>
                            <p class="section-name">Notes: </p>
                            <p></p>
                        </div>
                    </div>
                </div>`;
        $('#summary_right_content').append(row);
    }
    let accordions = document.getElementsByClassName("summary-accordion");
    for (i = 0; i < accordions.length; i++) {
        accordions[i].addEventListener("click", function () {
            this.classList.toggle("summary-active");
            let panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
})

// orderSaveBtn.addEventListener('click', () => {
//     $('#subtotal_modal').modal('show');
// })

// $('#subtotal_modal').on('show.bs.modal', () => {
//     if (window.location.pathname.includes('edit')) {
//         orderSubmitBtn.textContent = 'Save';
//     }

//     let hasCustomBillDate = getSelectedOption(document.querySelector('#bill_date'))['value'] == 'custom';
//     let isTearsheet = document.querySelector('#tearsheets').checked;
//     let hasOverrideAdCost = $('#overrideCost').val();

//     topLevelDetails = {
//         "Name": $('#name').val(),
//         "Account": getSelectedOption(document.querySelector('#account'))['name'],
//         "Ad Taker/Submitter": $('#adTaker').val(),
//         "Salesperson": getSelectedOption(document.querySelector('#salesperson'))['name'],
//         "Bill Date": getSelectedOption(document.querySelector('#bill_date'))['name'],
//         "Invoice Frequency": getSelectedOption(document.querySelector('#invoiceFrequency'))['name'],
//         "Notes": $('#notes').val(),
//         "Total Price": 0
//     };

//     if (hasCustomBillDate) topLevelDetails["Custom Bill Date"] = $('custom_billing_date').val();
//     if (hasOverrideAdCost) {
//         topLevelDetails["Override Ad Cost"] = `$${$('#overrideCost').val()}`;

//         priceValue.textContent = $('#overrideCost').val();
//         topLevelDetails['Total Price'] = $('#overrideCost').val();
//     }

//     topLevelDetails["Tearsheets"] = isTearsheet ? "Yes" : "No";

//     for (let [name, value] of Object.entries(topLevelDetails)) {
//         if (name == 'Total Price') continue;
//         $('#summary_topLevel tbody').append(`
//         <tr>
//                 <td>${name}</td>
//                 <td>${value}</td>
//             </tr>`)
//     }

//     let entries = Object.entries(publicationOrderData);
//     for (let i = 0; i < entries.length; i++) {
//         const publicationName = entries[i][0];
//         const detailsObj = entries[i][1];
//         // console.log(detailsObj)

//         let publicationDiv = $('<div class="panel panel-default publication-details"></div>')
//         publicationDiv.append(`<div class="panel-heading">
//                                     <h4 class="panel-title">
//                                         <a data-toggle="collapse" data-parent="#summary_accordion" href="#heading${i}">
//                                             ${publicationName}</a>
//                                     </h4>
//                                 </div>
//                                 <div id="heading${i}" class="panel-collapse collapse">
//                                     <div class="panel-body">
//                                         <div id="publication${i}-details"></div>
//                                     </div>
//                                 </div>`);
//         $('#summary_accordion').append(publicationDiv);

//         let detailsTable = $(`<table> `);
//         let headers = Object.keys(detailsObj);

//         for (let j = 0; j < headers.length; j++) {
//             let currentLabel = detailsObj[headers[j]]['label'];

//             if (currentLabel != undefined) {
//                 switch (currentLabel) {
//                     case 'Dates':
//                         detailsTable.append(`<tr>
//                                             <td>${currentLabel}</td>
//                                             <td>${detailsObj[headers[j]]['value']}</td>
//                                         </tr>`);
//                         break;
//                     case 'Ad Rate':
//                         let regex = /\$(.*?)\//;

//                         let rateName = detailsObj[headers[j]]['name'];
//                         let rateAmount = parseFloat(regex.exec(detailsObj[headers[j]]['name'])[1]);
//                         let unitLabel = detailsObj[headers[j]]['units']['label'];
//                         let unitValue = detailsObj[headers[j]]['units']['value'];

//                         topLevelDetails['Total Price'] += parseFloat(unitValue) * parseFloat(rateAmount);

//                         detailsTable.append(`<tr>
//                                             <td>${currentLabel}</td>
//                                             <td>${rateName} - (${unitValue} ${unitLabel})</td>
//                                         </tr>`);
//                         break;
//                     default:
//                         detailsTable.append(`<tr>
//                                                 <td>${currentLabel}</td>
//                                                 <td>${detailsObj[headers[j]]['name']}</td>
//                                             </tr>`);
//                         break;
//                 }
//             }
//         }
//         $(`#publication${i}-details`).append(detailsTable);
//     }
//     priceValue.textContent = topLevelDetails['Total Price'];
// });

// $('#subtotal_modal').on('hide.bs.modal', () => {
//     $('#summary_topLevel tbody').empty();
//     $('#summary_accordion').empty();
// });

// const handleOrderSubmit = e => {

//     if (isEmpty(publicationOrderData)) {
//         alert('Error. Cannot submit without selecting a publication. Please try again.');
//         return;
//     }

//     fetch(`/advertising/order/${orderId}/edit`, {
//         method: "POST",
//         credentials: "same-origin",
//         headers: {
//             "X-CSRFToken": getCookie('csrftoken'),
//             "Accept": "application/json",
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             topLevelDetails,
//             publicationOrderData
//         })
//     })
//         .then(res => {
//             if (!res.ok) {
//                 alert(res.statusText);
//             } else {
//                 return res.json();
//             }
//         })
//         .then(data => {
//             $('#subtotal_modal').modal('hide');
//             window.location.href = `/advertising/order/${orderId}`;
//         });

    // fetch('/advertising/order/new/', {
    //     method: "POST",
    //     credentials: "same-origin",
    //     headers: {
    //         "X-CSRFToken": getCookie('csrftoken'),
    //         "Accept": "application/json",
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({
    //         topLevelDetails,
    //         publicationOrderData
    //     })
    // })
    //     .catch(error => {
    //         console.error(error);
    //     })
    //     .then(res => res.json())
    //     .then(data => {
    //         console.log(data);
    //         let message = data.message;

    //         if (message.includes('Error')) {
    //             alert(data.message);
    //             return;
    //         } else {
    //             let orderId = data.orderId;

    //             alert(data.message);
    //             window.location.href = `/advertising/order/${orderId}`;
    //         }
    //     });
// }

// orderSubmitBtn.addEventListener('click', handleOrderSubmit);