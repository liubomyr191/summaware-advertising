console.log('UserRoles.js');

const roleTable = document.querySelector('#role-table');
const roleTableBody = roleTable.getElementsByTagName('tbody')[0];
const roleTableBodyRows = roleTableBody.getElementsByTagName('tr');

$('#userRoleModal').on('show.bs.modal', e => {
    let url = "/advertising/admin/user/" + userId + "/roles"
    $.ajax({
        type: "GET",
        url: url,
        data: userId,
        success: (result) => {
            let roles = result.roles;
            for (let i = 0; i < roleTableBodyRows.length; i++) {
                let checkbox = roleTableBodyRows[i].getElementsByTagName('input')[0];
                if (roles.includes(checkbox.name))
                    checkbox.checked = true;
            }
        },
        error: err => {
            console.error(err)
            alert(err.statusText)
            $('#userRoleModal').modal('hide');
        }
    })
});

for (let i = 0; i < roleTableBodyRows.length; i++) {
    let checkbox = roleTableBodyRows[i].getElementsByTagName('input')[0];
    let url = "/advertising/admin/user/" + userId + "/roles/save/";
    checkbox.addEventListener('click', e => {
        $.ajax({
            type: "POST",
            url: url,
            headers: {
                "X-CSRFTOKEN": getCookie('csrftoken')
            },
            data: { "role": e.target.name, "hasRole": e.target.checked },
            success: (result) => {
                console.log(result);
            },
            error: (result) => {
                console.error(result);
            }
        });
    })
}

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}


const roleCheckboxes = document.querySelectorAll('.role-checkbox');