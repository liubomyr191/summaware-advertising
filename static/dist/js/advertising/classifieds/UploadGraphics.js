const userCheckboxes = document.querySelectorAll('.user-upload');
const uploadTableBody = document.querySelector('#upload_permissions_table tbody');
const uploadUserRows = [...uploadTableBody.getElementsByTagName('tr')];

const selectFileInput = document.querySelector('#file');
const uploadedImage = document.querySelector('#uploadedImage');

const uploadSubmitBtn = document.querySelector('#upload_graphics_submit');

const deleteBtns = document.querySelectorAll('.delete-btn');

const deleteCheckboxes = document.querySelectorAll('.user-delete');
const deleteTableBody = document.querySelector('#delete_permissions_table tbody');
const deleteUserRows = [...deleteTableBody.getElementsByTagName('tr')];

const markActiveBtns = document.querySelectorAll('.mark-active');

let uploadedGraphic;
let graphicId;

$('#upload_permissions_modal').on('show.bs.modal', e => {
    fetch('/advertising/classifieds/graphics/permissions/upload/', {
        method: "GET"
    })
        .then(res => res.json())
        .then(data => {
            let permissionList = data.permission_list;
            for (const row of uploadUserRows) {
                for (let i = 0; i < permissionList.length; i++) {
                    if (permissionList[i] == row.dataset.userId) {
                        row.children[0].children[0].checked = true;
                    }
                }
            }
        });
});

$('#upload_permissions_modal').on('hide.bs.modal', e => {
    window.location.reload();
    $('#uploadedImage').attr('src', '');
});

$('#delete_permissions_modal').on('show.bs.modal', e => {
    fetch('/advertising/classifieds/graphics/permissions/delete/', {
        method: "GET"
    })
        .then(res => res.json())
        .then(data => {
            let permissionList = data.permission_list;
            for (const row of deleteUserRows) {
                for (let i = 0; i < permissionList.length; i++) {
                    if (permissionList[i] == row.dataset.userId) {
                        row.children[0].children[0].checked = true;
                    }
                }
            }
        });
});

$('#delete_permissions_modal').on('hide.bs.modal', e => {
    window.location.reload();
});

const handlePermissionChange = e => {
    let userId = e.target.parentElement.parentElement.dataset.userId;
    let hasPermission = e.target.checked;

    fetch(`/advertising/classifieds/graphics/permissions/upload/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            userId,
            hasPermission
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error')) {
                console.error(data.message);
                alert(data.message);
            }
            console.log(data);
        });
};

const handleDeletePermissionChange = e => {
    let userId = e.target.parentElement.parentElement.dataset.userId;
    let hasDeletePermission = e.target.checked;

    fetch(`/advertising/classifieds/graphics/permissions/delete/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            userId,
            hasDeletePermission
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message.includes('Error')) {
                console.error(data.message);
                alert(data.message);
            }
            console.log(data);
        });
};

const handleDelete = e => {
    e.preventDefault();
    graphicId = e.target.parentElement.dataset.graphicId;

    if (graphicId) {
        let confirmation = confirm('Are you sure you want to delete this graphic?');
        if (!confirmation) return;

        fetch(`/advertising/classifieds/graphics/action/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "graphicId": graphicId,
                "type": "delete"
            })
        })
            .then(res => res.json())
            .then(data => {
                if (data.message.includes('Error')) {
                    console.error(data.message);
                    alert(data.message);
                } else {
                    // console.log(data);
                    window.location.reload();
                }
            });
    }
};

const handleMarkActive = e => {
    e.preventDefault();
    graphicId = e.target.parentElement.dataset.graphicId;

    if (graphicId) {
        fetch(`/advertising/classifieds/graphics/action/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                graphicId,
                type: 'active'
            })
        })
            .then(res => res.json())
            .then(data => {
                if (data.message.includes('Error')) {
                    console.error(data.message);
                    alert(data.message);
                } else {
                    // console.log(data);
                    window.location.reload();
                }
            });
    }
}

function handleUploadGraphic() {
    if (this.files[0]) {
        uploadedGraphic = this.files[0];
        let picture = new FileReader();
        picture.readAsDataURL(this.files[0]);
        picture.addEventListener('load', function (event) {
            uploadedImage.style.display = 'block';
            uploadedImage.setAttribute('src', event.target.result);
        });
    }
};

const handleUpload = e => {
    e.preventDefault();

    let formData = new FormData();
    formData.append('image', $('#file')[0].files[0]);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'))
    formData.append('type', 'upload');

    $.ajax({
        type: 'POST',
        url: `/advertising/classifieds/graphics/action/`,
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        success: function (data) {
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#upload_graphics_modal').modal('show');
                window.location.reload();
            }
        },
        error: function (xhr, errmsg, err) {
            console.error(errmsg);
            return;
        }
    });
};

userCheckboxes.forEach(checkbox => checkbox.addEventListener('change', handlePermissionChange));
deleteCheckboxes.forEach(checkbox => checkbox.addEventListener('change', handleDeletePermissionChange));
deleteBtns.forEach(btn => btn.addEventListener('click', handleDelete));
markActiveBtns.forEach(btn => btn.addEventListener('click', handleMarkActive));
selectFileInput.addEventListener('change', handleUploadGraphic);
uploadSubmitBtn.addEventListener('click', handleUpload);