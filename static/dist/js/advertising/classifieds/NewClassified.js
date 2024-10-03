const accountSwitches = document.querySelectorAll('.account-switch');
const accountSelect = document.querySelector('#account-select');
const accountDetails = document.querySelector('#account-details');

const publicationSelect = document.querySelector('#publication');

const sizeInput = document.querySelector('#size');
const columnSection = document.querySelector('#column_section');
const columnInput = document.querySelector('#columns');
const numsColumnInput = document.querySelector('#column_length');
const conversionSwitches = document.querySelectorAll('input[name="conversion-type"');

const sizeDict = {
    "quarter_page": "Quarter Page",
    "half_page": "Half Page"
}

const salespersonSelect = document.querySelector('#salesperson');

const adTypeSelect = document.querySelector('#adType');

const datesSection = document.querySelector('#dates_section')
const datesInput = document.querySelector('#dates');

const recurringCheckbox = document.querySelector('#recurring-check');
const recurringSection = document.querySelector('#recurring_section');
const recurringStartDate = document.querySelector('#start_date');
const recurringAmount = document.querySelector('#recurring-amount');
const recurringTimePeriod = document.querySelector('#recurring-time');

const lineInput = document.querySelector('#lines');
const contentInput = document.querySelector('#content');
const contentPreview = document.querySelector('#content_preview');

const addGraphicBtns = document.querySelectorAll('.add-graphic-btn');

const addFrameCheckbox = document.querySelector('#addFrameInput');
const frameSizeInput = document.querySelector('#frameSizeInput');

const addInsetCheckbox = document.querySelector('#addInsetCheckbox');
const insetSelectGroup = document.querySelector('#insetSelectGroup');
const insetSelectInput = document.querySelector('#inset');

const adjustmentsTable = document.querySelector('#adjustments_table');
const adjustmentsTbody = adjustmentsTable.getElementsByTagName('tbody')[0];

const rateSelectBtn = document.querySelector('#rate_select_btn');
const rateSelectDiv = document.querySelector('#rate_select');

const adjustmentBtns = document.querySelectorAll('.action-btn');

const summaryModal = document.querySelector('#show_summary_modal');
const summaryData = {};

const submitBtn = document.querySelector('#classified_form_submit');

const publicationRateModal = document.querySelector('#publication_rate_modal');

const graphics = document.querySelectorAll('.graphic');

let selectedPubIds;
let selectedRates = {};

let ratePrices = [];

let graphicsIncluded = [];

let adjustmentList = [];

let totalPrice = 0.0;

let accountId;

accountSwitches.forEach(element => element.addEventListener('click', e => {
    accountSelect.style.display = e.target.id == 'account-yes' ? 'block' : 'none';
    accountDetails.style.display = e.target.id == 'account-no' ? 'block' : 'none';
}));

$('#dates').multiDatesPicker({
    minDate: 0,
    multidate: true,
    format: "yyyy-mm-dd",

});
CKEDITOR.on('instanceReady', function (e) {
    CKEDITOR.instances['id_content'].on('change', function (e) {
        let editorInput = this.getData();
        contentPreview.innerHTML = editorInput;
    })
});

let img;
addGraphicBtns.forEach(btn => btn.addEventListener('change', function (e) {
    img = $(this).parent().find('img')[0];
    let file_id = img.getAttribute('file_id');
    if (e.target.checked) {
        contentPreview.appendChild(img.cloneNode(true));
        graphicsIncluded.push(img.src);
    } else {
        img = $('#content_preview').find('img[file_id=' + file_id + ']').get(0);
        contentPreview.removeChild(img);
        graphicsIncluded = graphicsIncluded.filter(graphic => graphic != img.src)
    }
    return false;
}))

addFrameCheckbox.addEventListener('click', e => {
    if (e.target.checked) {
        frameSizeInput.style.display = 'block';
    } else {
        frameSizeInput.style.display = 'none';
        frameSize.value = null;
        contentPreview.style.border = 'none';
        summaryPreview.style.border = 'none';
    }
});

frameSizeInput.addEventListener('input', e => {
    let frameWidth = e.target.value;
    summaryData['frameWidth'] = e.target.value;
    contentPreview.style.border = frameWidth == '' ? 'none' : `${frameWidth}px solid black`;
    summaryPreview.style.border = frameWidth == '' ? 'none' : `${frameWidth}px solid black`;
});

accountSelect.addEventListener('input', e => {
    accountId = e.target.value;
    if (accountId) {
        fetch(`/advertising/ajax/account/${e.target.value}/salesperson/`, {
            method: "GET"
        })
            .then(res => res.json())
            .then(data => {
                if (data.message.includes('Error.')) alert(data.message);
                if (data.salesperson_details) {
                    let salesperson = data.salesperson_details;
                    selectOption(salespersonSelect, salesperson.id);
                }
            })
            .catch(err => console.error(err));
    }
});

sizeInput.addEventListener('change', e => {
    if (e.target.value == 'column_based') {
        columnSection.style.display = 'block';
    } else {
        columnSection.style.display = 'none';
        columnInput.value = 0;
    }
})

addInsetCheckbox.addEventListener('click', e => {
    if (e.target.checked) {
        insetSelectGroup.style.display = 'block';
    } else {
        insetSelectGroup.style.display = 'none';
        setDefaultOption(insetSelectInput);
        contentPreview.style.padding = 0;
        summaryPreview.style.padding = 0;
    }
});

insetSelectInput.addEventListener('input', e => {
    let insetAmount = e.target.value;
    summaryData['insetAmount'] = e.target.value;
    contentPreview.style.padding = insetAmount;
    summaryPreview.style.padding = insetAmount;
});

/* Adjustments Table */
publicationSelect.addEventListener('change', e => {
    selectedPubIds = [...e.target.selectedOptions].map(pub => pub.value);
    clearFrameWidth();
    clearInset();

    fetch(`/advertising/classifieds/adjustments/publications/?publication[]=${selectedPubIds}`, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            if (data.adjustments) {
                $('#adjustments_table tbody').empty();

                const adjustments = data.adjustments;
                const length = data.adjustments.length;

                for (let i = 0; i < length; i++) {
                    addRow(adjustments[i]);
                }

                // adjustmentBtns.forEach(checkbox => checkbox.addEventListener('click', handleAdjustment));
            }
        });

    if (selectedPubIds.length == 1) {
        fetch(`/advertising/publications/${selectedPubIds[0]}/styles/`, {
            method: "GET"
        })
            .then(res => res.json())
            .then(data => {
                // console.log(data);
                let details = data.details;

                if (data.message.includes('Error.')) {
                    console.error(data.message);
                } else {
                    frameSizeInput.style.display = 'block';
                    addFrameCheckbox.checked = true;
                    frameSize.value = details.frame_width;
                    summaryData['frameWidth'] = details.frame_width;
                    contentPreview.style.border = details.frame_width == '' ? 'none' : `${details.frame_width}px solid black`;
                    summaryPreview.style.border = details.frame_width == '' ? 'none' : `${details.frame_width}px solid black`;

                    insetSelectGroup.style.display = 'block';
                    addInsetCheckbox.checked = true;
                    selectOption(insetSelectInput, details.inset);
                    summaryData['insetAmount'] = details.inset;
                    contentPreview.style.padding = `${details.inset}px`;
                    summaryPreview.style.padding = `${details.inset}px`;
                }
            });
    } else {
        clearFrameWidth();
        clearInset();
    }
});

const clearFrameWidth = () => {
    frameSizeInput.style.display = 'none';
    addFrameCheckbox.checked = false;
    frameSize.value = 0;
    contentPreview.style.border = 'none';
    summaryPreview.style.border = 'none';
    // TODO - remove the frame width key from summaryData
}

const clearInset = () => {
    insetSelectGroup.style.display = 'none';
    addInsetCheckbox.checked = false;
    setDefaultOption(insetSelectInput);
    contentPreview.style.padding = 0;
    summaryPreview.style.padding = 0;
}

const addRow = data => {
    const keys = Object.keys(data);
    let row = adjustmentsTbody.insertRow(0);
    for (let index = 0; index < keys.length; index++) {
        let dataName = keys[index];
        let cell = row.insertCell(index);
        let cellContent = '';

        if (dataName != 'publication') {
            if (dataName == 'amount') {
                switch (data['value_type']) {
                    case 'amount':
                        cellContent = `$${data['amount']}`;
                        break;
                    case 'percentage':
                        cellContent = `${data['amount']}%`;
                        break;
                }
            } else {
                cellContent = data[dataName];
            }
        } else {
            cellContent = data['publication']['name'];
        }
        cell.innerHTML = cellContent;
    }
    let actionCell = row.insertCell(keys.length)
    actionCell.innerHTML = `<input type='checkbox' class='action-btn' data-adjustment-id='${data['id']}'/>`

    actionCell.addEventListener('click', handleAdjustment);
}

function handleAdjustment(e) {
    let adjustmentId = e.target.dataset.adjustmentId;
    let adjustment;
    let price;
    if (adjustmentId == undefined) return;
    fetch(`/advertising/classifieds/adjustments/${adjustmentId}/?adjustmentId=${adjustmentId}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            adjustment = data.adjustment;
            price = Number(adjustment.amount);

            if (e.target.checked) {
                adjustmentList.push(adjustment);

                // if the adjustment amount is only applied to the overall order
                if (adjustment.apply_level == 'order') {
                    // if the type is an amount, the entire amount is applied to the total price
                    if (adjustment.value_type == 'amount') {
                        // if the type is debit multiply the total price of the order and add it to the totalc price
                        if (adjustment.value_type == 'debit')
                            totalPrice += price;
                        else if (adjustment.value_type == 'credit')
                            // if the type is credit multiply the total price of the order and subtract it to the totalc price
                            totalPrice -= price;
                    } else if (adjustment.value_type == 'percentage') {
                        // if the type is a percentage, multiply the total price of the order by that percentage
                        if (adjustment.value_type == 'debit')
                            totalPrice += (totalPrice * (price / 100))
                        else if (adjustment.value_type == 'credit')
                            // if the type is credit multiply the total price of the order and subtract it to the totalc price
                            totalPrice -= (totalPrice * (price / 100));
                    }

                } else if (adjustment.apply_level == 'insertion') {
                    // if the  adjustment amount is applied to every insertion

                }
                console.log('Adjustment added. Price is: ' + totalPrice);
            } else {
                for (let i = 0; i < adjustmentList.length; i++) {
                    let adjustment = adjustmentList[i];

                    // if the adjustment amount is only applied to the overall order
                    if (adjustment.apply_level == 'order') {
                        // if the type is an amount, the entire amount is applied to the total price
                        if (adjustment.value_type == 'amount') {
                            // if the type is debit multiply the total price of the order and add it to the totalc price
                            if (adjustment.value_type == 'debit') {
                                console.log('Adjustment amount: ' + price)
                                totalPrice = totalPrice - price;
                                console.log('Total price: ' + totalPrice)
                            }
                            else if (adjustment.value_type == 'credit')
                                // if the type is credit multiply the total price of the order and subtract it to the totalc price
                                totalPrice += price;
                        } else if (adjustment.value_type == 'percentage') {
                            // if the type is a percentage, multiply the total price of the order by that percentage
                            if (adjustment.value_type == 'debit')
                                totalPrice -= (totalPrice * (price / 100))
                            else if (adjustment.value_type == 'credit')
                                // if the type is credit multiply the total price of the order and subtract it to the totalc price
                                totalPrice += (totalPrice * (price / 100));
                        }

                    } else if (adjustment.apply_level == 'insertion') {
                        // if the  adjustment amount is applied to every insertion

                    }
                }
                adjustmentList = adjustmentList.filter(adjustment => adjustment.id != adjustmentId);
                console.log('Adjustment removed. Price is: ' + totalPrice)
            }
        });
}

recurringCheckbox.addEventListener('change', e => {
    if (e.target.checked) {
        datesInput.disabled = true;
        datesInput.value = '';
        datesSection.style.display = 'none';

        recurringSection.style.display = 'block';
    } else {
        datesSection.style.display = 'block';
        datesInput.disabled = false;

        recurringSection.style.display = 'none';
        recurringStartDate.value = '';
        recurringAmount.value = null;
        setDefaultOption(recurringTimePeriod);
    }
})

$('#publication_rate_modal').on('show.bs.modal', () => {
    // TODO - refactor this to only show the alert message if no selected publications 
    // currently also shows the empty modal and a 500 error in the console
    if (selectedPubIds == undefined || selectedPubIds == 'undefined') {
        alert('Error. Please select publications first.');
        return;
    }
    fetch(`/advertising/classifieds/rates/?publications[]=${selectedPubIds}`, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            let rates = data.rates;
            for (const pubIndex of selectedPubIds) {
                if (rates[pubIndex].length) {
                    let publicationName = rates[pubIndex][0].publication;

                    let div = document.createElement('div');
                    div.classList.add('form-group');

                    let label = document.createElement('label');
                    label.innerHTML = `${publicationName} rates`;
                    label.htmlFor = `publication-${pubIndex}-rates`;

                    let select = document.createElement('select');
                    select.classList.add('form-control');
                    select.id = `publication-${pubIndex}-rates`;
                    select.name = `publication-${pubIndex}-rates`;
                    select.form = '#new_classified_form';

                    let option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'Select a rate...';

                    select.appendChild(option);

                    for (let i = 0; i < rates[pubIndex].length; i++) {
                        let rate = rates[pubIndex][i]['rate'];
                        let option = document.createElement('option');
                        option.value = rate.id;
                        option.textContent = `${rate.name} - $${rate.unit_price}/line`;

                        select.appendChild(option);

                        ratePrices.push(
                            {
                                "publication": publicationName,
                                "rate": rate.id
                            }
                        );
                    }
                    rateSelectDiv.appendChild(div).appendChild(label).appendChild(select);

                    select.addEventListener('change', e => {
                        let value = e.target.value;
                        let text = e.target.options[e.target.selectedIndex].text;

                        selectedRates[publicationName] = {
                            "publication": {
                                'name': publicationName,
                                'id': pubIndex
                            },
                            'rate': {
                                'name': text,
                                'id': value,
                            }
                        }
                    });
                }
            }
        });
});



$('#publication_rate_modal').on('hide.bs.modal', () => {
    $('#rate_select').empty();
});

// TODO - implement a search function to search for adjustments

/* -----------------------------------
    Summary Modal 
 ------------------------------------- */

const summaryTable = document.querySelector('#summary-table');
const summaryTbody = summaryTable.getElementsByTagName('tbody')[0];

const summaryPreview = document.querySelector('#summary_preview');
const totalPriceSpan = document.querySelector('#total_price');

$('#show_summary_modal').on('show.bs.modal', e => {
    let account = document.querySelector('#account');
    let classification = document.querySelector('#classification');
    let submitterInput = document.querySelector('#submitter');
    let notesInput = document.querySelector('#notes');

    // console.log(countTextLines(contentPreview))

    for (const acctSwitch of accountSwitches) {
        if (acctSwitch.id == 'account-yes') {
            for (let i = 0; i < account.options.length; i++) {
                let option = account.options[i];
                if (option.selected) {
                    summaryData['account'] = option.textContent;
                }
            }
        } else {
            summaryData['name'] = $('#name').val();
            summaryData['email'] = $('#email').val();
            summaryData['phone'] = $('#phone').val();
        }
    }

    for (let i = 0; i < classification.options.length; i++) {
        let option = classification.options[i];
        if (option.selected) {
            summaryData['classification'] = (option.textContent).trim();
        }
    }

    let selectedPublications = [...publicationSelect.selectedOptions].map(pub => pub.textContent);
    summaryData['publications'] = selectedPublications.join(', ');
    summaryData['publicationIds'] = selectedPubIds;

    summaryData['Ad Taker/Submitter'] = submitterInput.value;

    for (let i = 0; i < salespersonSelect.options.length; i++) {
        let option = salespersonSelect.options[i];
        if (option.selected) {
            summaryData['salesperson'] = option.textContent;
        }
    }

    if (recurringCheckbox.checked) {
        let inputs = document.getElementsByTagName("input");
        let weekdayDict = {
            "sunday": "Sun",
            "monday": "Mon",
            "tuesday": "Tues",
            "wednesday": "Wed",
            "thursday": "Thur",
            "friday": "Fri",
            "saturday": "Sat"
        }

        weekdayArray = [];
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].name.indexOf('recurr-') == 0) {
                let name = inputs[i].name.split('-')[1];
                let isChecked = inputs[i].checked;

                if (isChecked) weekdayArray.push(weekdayDict[name]);
            }
        }
        if (weekdayArray.length) {
            summaryData['dates'] = `${recurringAmount.value} ${getSelectedOption(recurringTimePeriod)} starting ${recurringStartDate.value} (${weekdayArray.join(',')})`;
            summaryData['weekday-array'] = weekdayArray;
        } else {
            summaryData['dates'] = `${recurringAmount.value} ${getSelectedOption(recurringTimePeriod)} starting ${recurringStartDate.value}`;
        }

    } else {
        summaryData['dates'] = datesInput.value;
    }

    if (getSelectedOption(sizeInput) == 'column_based') {
        let conversionUnit;
        for (const convSwitch of conversionSwitches) {
            if (convSwitch.checked) {
                if (convSwitch.id == 'con-col-in') {
                    conversionUnit = 'column inches';
                } else if (convSwitch.id == 'con-in') {
                    conversionUnit = 'inches';
                }
            }
        }
        if (column_length.value != undefined || column_length.value == 0) {
            summaryData['size'] = `${columnInput.value} columns (each ${column_length.value} ${conversionUnit})`;
        } else {
            summaryData['size'] = `${columnInput.value} columns`;
        }

    } else {
        summaryData['size'] = sizeDict[getSelectedOption(sizeInput)];
    }

    for (let i = 0; i < adTypeSelect.options.length; i++) {
        let option = adTypeSelect.options[i];
        if (option.selected) summaryData['Ad Type'] = option.textContent;
    }

    summaryData['notes'] = notesInput.value;

    summaryData['graphics'] = graphicsIncluded;

    summaryData['Total Lines'] = lineInput.value;

    summaryData['text'] = contentPreview.innerHTML;
    summaryData['text-styling'] = contentPreview.getAttribute('style');

    summaryData['publication-rates'] = selectedRates;

    for (let [name, data] of Object.entries(selectedRates)) {
        summaryData[`${name} rate`] = data.rate.name;
    }

    for (let [key, value] of Object.entries(summaryData)) {
        if ((key == 'text') || (key == 'publicationIds') || (key == 'publication-rates') ||
            (key == 'frameWidth') || (key == 'insetAmount') || (key == 'graphics') || (key == 'text-styling') ||
            (key == 'weekday-array')) continue;
        if (value == '') continue;
        if (summaryData[key] == 'undefined') continue;

        let row = summaryTbody.insertRow(0);

        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);

        cell1.innerHTML = title(key);
        cell2.innerHTML = summaryData[key];
    }
    selectedPublications = [...publicationSelect.selectedOptions].map(pub => pub.textContent);
    summaryPreview.innerHTML = contentPreview.innerHTML;

    for (let [name, data] of Object.entries(selectedRates)) {
        let rate = data.rate;

        price = rate.name.split('$')[1].split('/')[0];
        totalPrice += Number(price) * lineInput.value;
    }

    totalPriceSpan.textContent = totalPrice;
    summaryData['Total Price'] = totalPrice;

});

$('#show_summary_modal').on('hide.bs.modal', e => {
    $('#summary-table tbody').html('');
    $('#summary_preview').html('');
    totalPrice = 0;
});

submitBtn.addEventListener('click', async e => {
    e.preventDefault();

    fetch(`/advertising/account/${accountId}/`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        method: 'GET'
    })
        .then(res => {
            if (!res.ok) {
                console.log(res.status)
            } else {
                return res.json();
            }
        })
        .then(data => {
            console.log(data);

            if (data.days > 30) {
                submitOrder();
            } else {
                let confirmation = confirm("The account selected is less than 30 days old. Do you wish to proceed?");
                if (confirmation) {
                    summaryData['needs-manager-override'] = true
                    submitOrder();
                } else {
                    return;
                }
            }
        })
        .catch(err => console.error(err));
}, false);

const calculateContentHeight = (element, scanAmount) => {
    let origHeight = element.style.height;
    let height = element.offsetHeight;
    let scrollHeight = element.scrollHeight;
    let overflow = element.style.overflow;

    if (height >= scrollHeight) {
        element.style.height = (height + scanAmount) + 'px';
        element.style.overflow = 'hidden';
        if (scrollHeight < element.scrollHeight) {
            while (element.offsetHeight >= element.scrollHeight) {
                element.style.height = (height -= scanAmount) + 'px';
            }
            while (element.offsetHeight < element.scrollHeight) {
                element.style.height = (height++) + 'px';
            }
            element.style.height = origHeight;
            element.style.overflow = overflow;
            return height;
        }
    } else {
        return scrollHeight;
    }
}

const countTextLines = div => {
    // let divHeight = div.offsetHeight
    // let lineHeight = parseInt(div.style.lineHeight);
    // let lines = divHeight / lineHeight;
    // return Math.ceil(lines);

    // let lineCount = div.textContent.split(/\n/);
    // let numLines = lineCount.filter(function (a) {
    //     var b = a.replace(/ /g, '');
    //     return (typeof (b) == 'string' && b != '')
    // });

    // return numLines.length;

    // let el = document.getElementById('content');
    // let divHeight = el.offsetHeight
    // let lineHeight = parseInt(el.style.lineHeight);

    // console.log(el.style.lineHeight);
    // let lines = divHeight / lineHeight;
    // return lines;
}

function getStyleById(id) {
    return getAllStyles(document.getElementById(id));
}
function getAllStyles(elem) {
    if (!elem) return []; // Element does not exist, empty list.
    var win = document.defaultView || window, style, styleNode = [];
    if (win.getComputedStyle) { /* Modern browsers */
        style = win.getComputedStyle(elem, '');
        for (var i = 0; i < style.length; i++) {
            styleNode.push(style[i] + ':' + style.getPropertyValue(style[i]));
            //               ^name ^           ^ value ^
        }
    } else if (elem.currentStyle) { /* IE */
        style = elem.currentStyle;
        for (var name in style) {
            styleNode.push(name + ':' + style[name]);
        }
    } else { /* Ancient browser..*/
        style = elem.style;
        for (var i = 0; i < style.length; i++) {
            styleNode.push(style[i] + ':' + style[style[i]]);
        }
    }
    return styleNode;
}

const submitOrder = () => {
    // console.log(summaryData);
    fetch('/advertising/classifieds/new/', {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(summaryData)
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Success')) {
                $('#show_summary_modal').modal('hide');
                window.location.href = `/advertising/classifieds/${data.id}`;
            } else {
                alert('An error has occurred creating the classified ad. Please try again.');
                console.error(data.message);
                return;
            }
        })
        .catch(err => console.error(err))
}

// TODO - if the recurring time period select is set to 'insertions', clear the weekday checkboxes and set the display to none

let dragged;
graphics.forEach(graphic => {
    graphic.addEventListener("drag", event => {
        event.dataTransfer.setData("text", event.target.id);
    });
    graphic.addEventListener("dragstart", (event) => {
        dragged = event.target;
    });
});

contentPreview.addEventListener("dragover", (event) => {
    event.preventDefault();
}, false);

contentPreview.addEventListener('drop', event => {
    event.preventDefault();

    let data = event.dataTransfer.getData("text");
    event.target.appendChild(document.getElementById(data));

    // TODO - on drop of the image in the content preview box, add it to the includedGraphics array
});

contentPreview.addEventListener("drop", (event) => {
    event.preventDefault();
    event.target.appendChild(dragged);
});

selectOption(adTypeSelect, 1);
