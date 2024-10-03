const publicationSelect = document.querySelector('#publications')
const rateSelectDiv = document.querySelector('#rate_select');

const sizeInput = document.querySelector('#size');
const columnInput = document.querySelector('#columns');
const columnSection = document.querySelector('#column_section');

const datesSection = document.querySelector('#dates_section')
const datesInput = document.querySelector('#dates');

const recurringCheckbox = document.querySelector('#recurring-check');
const recurringSection = document.querySelector('#recurring_section');
const recurringStartDate = document.querySelector('#start_date');
const recurringAmount = document.querySelector('#recurring-amount');
const timePeriodSelect = document.querySelector('#recurring-time');

// const startDate = document.querySelector('#start_date');
// const endDateSection = document.querySelector('#end_date_section');
// const endDate = document.querySelector('#end_date');

$('#dates').multiDatesPicker({
    minDate: 0,
    multidate: true,
    format: "yyyy-mm-dd",
});
$('#dates').multiDatesPicker('addDates', dateArray);

CKEDITOR.on('instanceReady', function (e) {
    CKEDITOR.instances['id_content'].on('change', function (e) {
        let editorInput = this.getData();

        contentPreview.innerHTML = editorInput;
    })
});

const sizeDict = {
    "quarter_page": "Quarter Page",
    "half_page": "Half Page",
    'column_based': "Column Based"
}
sizeInputValue = getKeyByValue(sizeDict, sizeInputValue);

let selectedPubIds = getSelectedOptions(publicationSelect);

selectedRates = selectedRates.replace(/'/g, '"') //replacing all ' with "
selectedRates = JSON.parse(selectedRates);

sizeInput.addEventListener('change', e => {
    if (e.target.value == 'column_based') {
        columnSection.style.display = 'block';
    } else {
        columnSection.style.display = 'none';
        columnInput.value = 0;
    }
});

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
        setDefaultOption(timePeriodSelect);
    }
})

$('#publication_rate_modal').on('show.bs.modal', e => {
    fetch(`/advertising/classifieds/rates/?publications[]=${selectedPubIds}`, {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            // console.log(data);

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
                    }
                    rateSelectDiv.appendChild(div).appendChild(label).appendChild(select);
                }
            }

            for (let i = 0; i < selectedRates.length; i++) {
                let pubRate = selectedRates[i];
                let pubRateSelect = document.querySelector(`#publication-${pubRate['publication']}-rates`);

                selectOption(pubRateSelect, pubRate['rate']);
            }
        });
});

$('#publication_rate_modal').on('hide.bs.modal', e => {
    $('#rate_select').empty();
});

selectOption(sizeInput, sizeInputValue);
if (getSelectedOption(sizeInput) == 'column_based') {
    columnSection.style.display = 'block';
    columnInput.value = columnsValue;
}

if (isRecurring) {
    datesSection.style.display = 'none';
    recurringCheckbox.checked = true;
    recurringSection.style.display = 'block';
    selectOption(timePeriodSelect, recurringTimePeriod);
} else {

}