const publications = document.querySelector('#publication');
const rateSubmitBtn = document.querySelector('#rate-submit-btn');

const selectAllPublications = document.querySelector('#select_all_publications');

let glCodes;
let selectedGLCodes = {}; 
let selectedPubIds;

$('#gl-code-btn-modal').click(e => {
    e.preventDefault();
    $('#gl-code-modal').modal('show');
});

$('#gl-code-modal').on('show.bs.modal', () => {
    $('#publication-gl-codes-select').empty();
    selectedPubIds = getSelectValues(publications);

    if (!(selectedPubIds.length)) {
        return;
    }

    getGLCodes(selectedPubIds);
});

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

const getSelectNames = select => {
    var result = [];
    var options = select && select.options;
  
    for (let i=0; i < options.length; i++) {
      option = options[i];
  
      if (option.selected) {
        console.log(select)
        result.push(select.labels[0].textContent.trim());
      }
    }
    return result;
}

const getGLCodes = (codeList) => {
    $.ajax({
        type: "GET",
        url: '/advertising/ajax/gl-codes/',
        data: { "publications[]": codeList },
        success: result => {
            glCodes = result.gl_codes ? result.gl_codes : {};
            populateGLCodes(glCodes);
        }, 
        error: error => {
            alert(error.statusText)
        }
    });
}

const populateGLCodes = (codes) => {
    if (isEmptyObject(codes)) console.error('Codes provided are not an object');
    
    let codeOptions = '';
    let publicationNames = Object.keys(codes);
    publicationNames.forEach((name, index) => {
        codeOptions += `<div class="form-group">
                            <label for="pub-${selectedPubIds[index]}-gl-code">${name}</label>
                            <select class="form-control gl-codes-select" id="pub-${selectedPubIds[index]}-gl-code" name="pub-${selectedPubIds[index]}-gl-code"></select>
                        </div>`;
    })
    $('#publication-gl-codes-select').append(codeOptions);

    let codeSelects = document.querySelectorAll('.gl-codes-select'); 
    for (let [key, value] of Object.entries(codes)) {
        console.log(codes)
        codeSelects.forEach(codeSelect => {
            let publicationName = codeSelect.labels[0].textContent.trim();
            let codes = value;

            if (publicationName == key) {
                if (codes.length) {
                    let option = document.createElement('option');
                    option.value = "";
                    option.text = "Select a GL Code...";
                    codeSelect.appendChild(option);
                    for (var i = 0; i < codes.length; i++) {
                        option = document.createElement("option");
                        option.value = codes[i].id;
                        option.text = String(codes[i].code) + " - " + codes[i].description;
                        if (Number(selectedGLCodes[publicationName]) == option.value) option.selected = true;
                        codeSelect.appendChild(option);
                    }
                } else {
                    var option = document.createElement("option");
                    option.value = "";
                    option.text = 'No codes found';
                    option.selected = true;
                    option.disabled = true;
                    codeSelect.appendChild(option);
                }
            }
        });
    }
    document.querySelectorAll('.gl-codes-select').forEach(select => {
        select.addEventListener('change', e => {
            let publicationName = select.labels[0].textContent.trim();
            let option = e.target.selectedOptions[0];
            if (!(option.label in selectedGLCodes)) {
                selectedGLCodes[publicationName] = option.value;
            }
            if (selectedGLCodes[publicationName] == '') {
                selectedGLCodes = removeKey(publicationName, selectedGLCodes);
            }
            
        })
    });
};

selectAllPublications.addEventListener('click', e => {
    let checked = e.target.checked;
    let publicationSelect = document.querySelector('#publication');

    for (let i = 0; i < publicationSelect.options.length; i++) {
        publicationSelect.options[i].selected = checked;
    }
})

rateSubmitBtn.addEventListener('click', e => {
    e.preventDefault();
    console.log($('#new_rate_form').serializeArray());

    $.ajax({
        type: "POST",
        url: '/advertising/rate/new/',
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        },
        data: $('#new_rate_form').serializeArray(),
        success: result => {
            console.log(result)
            window.location.href = `/advertising/rate/${result.rateId}`;
        },
        error: err => {
            console.error(err);
        }
    })
})

const isEmptyObject = obj => Object.keys(obj).length === 0;
const removeKey = (key, {[key]: _, ...rest}) => rest;

