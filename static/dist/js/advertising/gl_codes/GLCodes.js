const createGLCodeModal = document.querySelector('#create_gl_code_modal');
const createGLCodeForm = document.querySelector('#create_gl_code_form');
const createCode = document.querySelector('#code');
const createDescription = document.querySelector('#description');
const createPLType = document.querySelector('#pl_type');
const createSubmitBtn = document.querySelector('#create_gl_code_submit');

const editBtns = document.querySelectorAll('.edit-btn');

const editGLCodeModal = document.querySelector('#edit_gl_code_modal');
const editGLCodeForm = document.querySelector('#create_gl_code_form');
const editCode = document.querySelector('#editCode');
const editDescription = document.querySelector('#editDescription');
const editPLType = document.querySelector('#editPLType');
const editSubmitBtn = document.querySelector('#edit_gl_code_submit');

let codeId;

// Define the Gl code style feature
const GL_CODE_LENGTH = 7;
const GL_CODE_SEGMENT_LENGTH = [4, 3];

createSubmitBtn.addEventListener('click', e => {
    e.preventDefault();

    // TODO - validate that code is only 4 numerical digits before sending

    let glCode = createCode.value.replace(/\D/g, '');

    if(glCode.length != GL_CODE_LENGTH)  {
        alert("Please input the GL CODE correctly!");
        return;
    }

    if(createDescription.value.length < 1 )  {
        alert("Please input the description!");
        return;
    }

    if(createPLType.value.length < 1 )  {
        alert("Please input the P&L Type!");
        return;
    }

    fetch(`/advertising/gl-codes/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        // send only numerical gl code
        body: JSON.stringify({
            code: createCode.value,
            description: createDescription.value,
            pl_type : createPLType.value
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
    createPLType.value = '';
});

editBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        codeId = e.target.parentElement.parentElement.dataset.codeId
        $('#edit_gl_code_modal').modal('show');
    })
})

$('#edit_gl_code_modal').on('show.bs.modal', e => {
    console.log('editModal')
    if (codeId) {
        fetch(`/advertising/gl-codes/${codeId}/`, {
            method: 'GET'
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);

                let glCode = data.gl_code;

                // Display the formatted code
                editCode.value = glCode.code;
                editDescription.value = glCode.description;
                editPLType.value = glCode.pl_type;
            })
    }
});

editSubmitBtn.addEventListener('click', e => {

    let glCode = editCode.value.replace(/\D/g, '');

    if(glCode.length != GL_CODE_LENGTH)  {
        alert("Please input the GL CODE correctly!");
        return;
    }

    if(editDescription.value.length < 1 )  {
        alert("Please input the description!");
        return;
    }

    if(editPLType.value.length < 1 )  {
        alert("Please input the P&L Type!");
        return;
    }

    
    fetch(`/advertising/gl-codes/${codeId}/edit/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: editCode.value,
            description: editDescription.value,
            pl_type : editPLType.value
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

const searchInput = document.querySelector('#search-glcode');
const searchTableBody = document.querySelector('#gl_code_table_tbody');
const searchTableRows = searchTableBody.querySelectorAll('tr');
searchInput.addEventListener('keyup', () => {
    const searchValue = searchInput.value;
    searchCodes(searchValue)
});

const searchCodes = (searchValue) => {
    searchTableRows.forEach(row => {
        const rowTitle = row.querySelector('td:nth-child(2)').innerText;
        const rowCode = row.querySelector('td:nth-child(3)').innerText;

        if (searchValue === "") {
            row.style.display = '';
        } else if (!rowTitle.toLowerCase().includes(searchValue.toLowerCase()) && !rowCode.toLowerCase().includes(searchValue.toLowerCase()))
            row.style.display = 'none';
    });
}

// Function to format the code as xx-xxx-xx-xx-xxxx-xxx
function formatGLCode(inputElement) {
    
    
    
    let formatted = inputElement.value.replace(/\D/g, ''); // Remove non-numeric characters
    formatted = formatted.slice(0, GL_CODE_LENGTH); // Limit to GL_CODE_LENGTH characters

    let currentIndex = 0;
    
    // Format the code
    for (let i = 0; i < GL_CODE_SEGMENT_LENGTH.length; i++) {
        if (formatted.length > currentIndex + GL_CODE_SEGMENT_LENGTH[i]) {
            formatted = formatted.slice(0, currentIndex + GL_CODE_SEGMENT_LENGTH[i]) + '-' + formatted.slice(currentIndex + GL_CODE_SEGMENT_LENGTH[i]);
            currentIndex += GL_CODE_SEGMENT_LENGTH[i] + 1;
        }
    }
    
    // Replace the input value with the formatted string
    inputElement.value = formatted;
}

// Attach event listeners to input elements
createCode.addEventListener('input', () => {
    formatGLCode(createCode);
});

editCode.addEventListener('input', () => {
    formatGLCode(editCode);
});

