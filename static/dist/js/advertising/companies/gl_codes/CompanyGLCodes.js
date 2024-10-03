const createGLCodeModal = document.querySelector('#create_gl_code_modal');
const createGLCodeForm = document.querySelector('#create_gl_code_form');
const createCode = document.querySelector('#code');
const createDescription = document.querySelector('#description');
const createSubmitBtn = document.querySelector('#create_gl_code_submit');

const editBtns = document.querySelectorAll('.edit-btn');

const editGLCodeModal = document.querySelector('#edit_gl_code_modal');
const editGLCodeForm = document.querySelector('#create_gl_code_form');
const editCode = document.querySelector('#editCode');
const editDescription = document.querySelector('#editDescription');
const editSubmitBtn = document.querySelector('#edit_gl_code_submit');

let codeId;

createSubmitBtn.addEventListener('click', e => {
    e.preventDefault();

    // TODO - validate that code is only 4 numerical digits before sending

    fetch(`/advertising/company/${companyId}/gl-codes/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: createCode.value,
            description: createDescription.value
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#create_gl_code_modal').modal('hide');
                window.location.reload();
            }
        })
        .catch(err => console.error(err))
});

$('#create_gl_code_modal').on('hide.bs.modal', e => {
    createCode.value = '';
    createDescription.value = '';
});

editBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        codeId = e.target.parentElement.dataset.codeId;
        $('#edit_gl_code_modal').modal('show');
    })
})

$('#edit_gl_code_modal').on('show.bs.modal', e => {
    if (codeId) {
        fetch(`/advertising/company/${companyId}/gl-codes/${codeId}/`, {
            method: 'GET'
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);

                let glCode = data.gl_code;

                editCode.value = glCode.code;
                editDescription.value = glCode.description;
            })
    }
});

editSubmitBtn.addEventListener('click', e => {
    fetch(`/advertising/company/${companyId}/gl-codes/${codeId}/edit/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: editCode.value,
            description: editDescription.value
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#edit_gl_code_modal').modal('hide');
                window.location.reload();
            }
        })
        .catch(err => console.error(err))
})