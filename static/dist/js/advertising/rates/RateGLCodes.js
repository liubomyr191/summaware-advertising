const companySelect = document.querySelector('#company');
const rateSelect = document.querySelector('#rate');

const rateDetailsTable = document.querySelector('#rate_details_table');
const rateName = document.querySelector('#rate_name');
const rateRunDays = document.querySelector('#run_dates');
const rateUnitPrice = document.querySelector('#unit_price');
const rateUnitType = document.querySelector('#unit_type');
const rateActive = document.querySelector('#active');
const rateDefaultGLCode = document.querySelector('#default_gl_code');

const publicationGLCodeTable = document.querySelector('#publication_gl_code_table');
const glCodeTableBody = publicationGLCodeTable.getElementsByTagName('tbody')[0];

let rateId;
let companyId;

// companySelect.addEventListener('change', function (e) {
//     if (e.target.value != '') {
//         companyId = e.target.value;
//         checkForValues();
//     }
// });

rateSelect.addEventListener('change', function (e) {
    if (getSelectedOption(rateSelect) != '') {
        rateId = e.target.value;
        fetch(`/advertising/rate/${rateId}/details/`, {
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
                if (data.rate_details) {
                    let details = data.rate_details;

                    rateDetailsTable.style.display = 'block';
                    $('#publication_gl_code_table tbody').empty();
                    rateName.textContent = details.name;
                    rateRunDays.textContent = `${(new Date(details.start_date).toLocaleDateString())} - ${(new Date(details.start_date).toLocaleDateString())}`;
                    rateUnitPrice.textContent = `$${details.unit_price}`;
                    rateUnitType.textContent = details.unit_type;
                    rateActive.textContent = details.active ? 'Yes' : 'No';
                    rateDefaultGLCode.textContent = details.default_gl_code ? `${details.default_gl_code.code} - ${details.default_gl_code.description}` : 'None selected';
                }
                checkForValues();
            });
    } else {
        rateName.textContent = '';
        rateRunDays.textContent = '';
        rateUnitPrice.textContent = '';
        rateUnitType.textContent = '';
        rateActive.textContent = '';

        $('#publication_gl_code_table tbody').empty();

        rateDetailsTable.style.display = 'none';
    }
});

function checkForValues() {
    if (rateId) {
        fetch(`/advertising/rate/${rateId}/publication/gl-codes/`, {
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
                console.log(data)
                if (data.rate_publications) {
                    let publications = data.rate_publications;
                    if (publications) {
                        for (let i = 0; i < publications.length; i++) {
                            let row = '';

                            row += `<tr>
                                        <td>${publications[i].name}</td>
                                        <td data-publication=${publications[i].id}>
                                            <select class="gl-code-select"></select>
                                        </td>
                                    </tr>`;
                            $('#publication_gl_code_table tbody').append(row);
                        }
                    } else {
                        $('#publication_gl_code_table tbody').append(`<tr><td colspan="2">No publications found</td></tr>`);
                    }
                }

                let glCodeSelect = document.querySelectorAll('.gl-code-select');
                if (data.gl_codes) {
                    let codes = data.gl_codes;

                    for (let i = 0; i < glCodeSelect.length; i++) {
                        let opt = document.createElement("option");
                        opt.value = '';
                        opt.textContent = `Select a GL Code ...`;
                        glCodeSelect[i].add(opt);

                        for (let j = 0; j < codes.length; j++) {
                            let opt = document.createElement("option");
                            opt.value = codes[j].id;
                            opt.textContent = `${codes[j].code} - ${codes[j].description}`;

                            glCodeSelect[i].add(opt);
                        }

                        glCodeSelect[i].addEventListener('change', function (e) {
                            if (e.target.value != '') {
                                let glCodeId = e.target.value;
                                let publicationId = e.target.parentElement.dataset.publication;

                                fetch(`/advertising/rate/${rateId}/publication/gl-codes/`, {
                                    method: "POST",
                                    credentials: "same-origin",
                                    headers: {
                                        "X-CSRFToken": getCookie('csrftoken'),
                                        "Accept": "application/json",
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({ glCodeId, publicationId })
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
                                    })
                            }
                        })
                    }
                }

                if (data.selected_codes) {
                    let selectedCodes = data.selected_codes;
                    for (let i = 0; i < glCodeSelect.length; i++) {
                        let selectPubId = glCodeSelect[i].parentElement.dataset.publication;
                        selectedCodes.forEach(code => {
                            if (code.publication == selectPubId) {
                                selectOption(glCodeSelect[i], code.gl_code);
                            }
                        })
                    }
                }
            })
            .catch(err => {
                console.error(err);
                alert(err.statusText);
                return;
            });
    } else {
        return false;
    }
}