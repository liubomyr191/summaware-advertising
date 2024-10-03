const sectionNameInput = document.querySelector('#section_name');
const sectionNumPagesInput = document.querySelector('#section_number_pages');

const createSectionForm = document.querySelector('#create_section_form');
const createSectionSubmitBtn = document.querySelector('#create_section_submit');

const editBtns = document.querySelectorAll('.edit-section');

const editSectionNameInput = document.querySelector('#edit_section_name');
const editSectionNumPagesInput = document.querySelector('#edit_section_number_pages');
const editSectionActiveCheckbox = document.querySelector('#edit_active');

const editSectionForm = document.querySelector('#edit_section_form');
const editSectionSubmitBtn = document.querySelector('#edit_section_submit');

let sectionId;

const handleCreate = e => {
    e.preventDefault();
    if (!sectionNameInput.value || !sectionNumPagesInput.value) {
        alert('Please fill out both the fields before submitting');
        return;
    }

    fetch(`/advertising/publication/${publication_id}/sections/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: sectionNameInput.value,
            number_pages: sectionNumPagesInput.value,
            publication: publication_id
        })
    })
        .then(res => {
            if (!res.ok) {
                alert(res.statusText);
            } else {
                return res.json();
            }
        })
        .then(data => {
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#create_section_modal').modal('hide');
                window.location.reload();
            }
        })
};

$('#create_section_modal').on('hide.bs.modal', e => {
    $('#create_section_form')[0].reset();
});

const handleEdit = e => {
    fetch(`/advertising/publication/${publication_id}/sections/${sectionId}/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: editSectionNameInput.value,
            number_pages: editSectionNumPagesInput.value,
            active: editSectionActiveCheckbox.checked,
            publication: publication_id
        })
    })
        .then(res => {
            if (!res.ok) {
                alert(res.statusText);
            } else {
                return res.json();
            }
        })
        .then(data => {
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#edit_section_modal').modal('hide');
                window.location.reload();
            }
        })
}

createSectionSubmitBtn.addEventListener('click', handleCreate);

editBtns.forEach(btn => btn.addEventListener('click', e => {
    sectionId = e.target.parentElement.dataset.sectionId;
    $('#edit_section_modal').modal('show');
}));

$('#edit_section_modal').on('show.bs.modal', e => {
    if (sectionId) {
        fetch(`/advertising/publication/${publication_id}/sections/${sectionId}/`, {
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

                if (data.message.includes('Error.')) {
                    alert(data.message);
                    return;
                } else {
                    let section = data.section;

                    editSectionNameInput.value = section.name;
                    editSectionNumPagesInput.value = section.number_pages;

                    editSectionActiveCheckbox.checked = section.active;
                }
            });
    }
});

editSectionSubmitBtn.addEventListener('click', handleEdit)