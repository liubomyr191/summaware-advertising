const createStylesSubmit = document.querySelector('#create_styles_submit');
const editStylesSubmit = document.querySelector('#edit_styles_submit');

const createFontInput = document.querySelector('#font');
const createFontSizeInput = document.querySelector('#font_size');
const createInsetInput = document.querySelector('#inset');
const createFrameWidthInput = document.querySelector('#frame_width');

const editFontInput = document.querySelector('#editFont');
const editFontSizeInput = document.querySelector('#editFontSize');
const editInsetInput = document.querySelector('#editInset');
const editFrameWidthInput = document.querySelector('#editFrameWidth');

const handleCreateStyles = e => {
    e.preventDefault();

    fetch(`/advertising/publications/${publication_id}/styles/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "font": getSelectedOption(createFontInput),
            "font_size": getSelectedOption(createFontSizeInput),
            "inset": getSelectedOption(createInsetInput),
            "frame_width": createFrameWidthInput.value
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error.')) return;

            console.log(data);
            $('create_styles_modal').modal('hide');
            window.location.reload();
        })
}

const handleEditStyles = e => {
    e.preventDefault();

    fetch(`/advertising/publications/${publication_id}/styles/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "font": getSelectedOption(editFontInput),
            "font_size": getSelectedOption(editFontSizeInput),
            "inset": getSelectedOption(editInsetInput),
            "frame_width": editFrameWidthInput.value
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error.')) return;
            console.log(data);

            $('edit_styles_modal').modal('hide');
            window.location.reload();
        })
}
if (createStylesSubmit) {
    createStylesSubmit.addEventListener('click', handleCreateStyles);
} else {
    editStylesSubmit.addEventListener('click', handleEditStyles);
}
