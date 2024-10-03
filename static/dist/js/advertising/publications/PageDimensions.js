const newDimensionsSubmit = document.querySelector('#add_dimensions_submit');
const submitBtn = document.querySelector('#edit_dimensions_submit');

let publicationId;

$('#edit_dimensions_modal').on('show.bs.modal', e => {
    publicationId = e.target.dataset.publication;

    fetch(`/advertising/publication/${publicationId}/page-dimensions/`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            // "X-CSRFToken": csrf_token,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
        .then(res => res.json())
        .then(data => {
            if (data.dimensions) populateForm(data.dimensions);
        })
})

const populateForm = dimensions => {
    for (const [key, value] of Object.entries(dimensions)) {
        $(`#${key}`).val(value);
    }
}

const handleNewDimensionsSubmit = e => {
    fetch(`/advertising/publication/${publication_id}/page-dimensions/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            page_size: $('#newPageSize').val(),
            columns_per_page: $('#newColumnsPerPage').val(),
            column_width: $('#newColumnWidth').val(),
            page_width: $('#newPageWidth').val(),
            page_height: $('#newPageHeight').val(),
            page_border: $('#newPageBorder').val(),
            gutter_size: $('#newGutterSize').val(),
            column_inches: $('#newColumnInches').val(),
            inches: $('#newInches').val(),
            default_size: $('#newDefaultSize').val()
        }),
    })
        .catch(err => console.error(err))
        .then(res => res.json())
        .then(() => {
            $('#add_page_dimensions_modal').modal('hide');
            window.location.reload();
        })
}

const handleSubmit = e => {
    let formData = {
        "page_size": $('#page_size').val(),
        "columns_per_page": $('#columns_per_page').val(),
        "column_width": $('#column_width').val(),
        "page_width": $('#page_width').val(),
        "page_height": $('#page_height').val(),
        "page_border": $('#page_border').val(),
        "gutter_size": $('#gutter_size').val(),
        "column_inches": $('#column_inches').val(),
        "inches": $('#inches').val(),
        "default_size": $('#default_size').val()
    }
    fetch(`/advertising/publication/${publicationId}/page-dimensions/edit/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData),
    })
        .catch(err => console.error(err))
        .then(res => res.json())
        .then(() => {
            $('#edit_dimensions_modal').modal('hide');
            window.location.reload();
        })
}
newDimensionsSubmit ?
    newDimensionsSubmit.addEventListener('click', handleNewDimensionsSubmit) :
    submitBtn.addEventListener('click', handleSubmit);