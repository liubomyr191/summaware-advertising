const roleTable = document.querySelector('#role-table');
const roleTableBody = roleTable.getElementsByTagName('tbody')[0];
const roleTableBodyRows = roleTableBody.getElementsByTagName('tr');

const userInput = document.querySelector('#username');
const accountInput = document.querySelector('#account');

let userChoice;
let accountChoice;

const handleChange = e => {
    resetCheckboxes();

    let input = e.target.id;
    let inputValue = e.target.value;

    // TODO - make this a switch statement
    if(input == 'username') {
        userChoice = inputValue;
    } else if (input == 'account') {
        accountChoice = inputValue;
    }

    if (inputValue == '') {
        if (input == 'username') {
            userChoice = '';
        } else if (input == 'account') {
            accountChoice == '';
        }
    }
    
    if (userChoice && accountChoice) {
        let url = `/advertising/admin/user/${userChoice}/roles`;
        $.ajax({
            type: "GET",
            url: url,
            data: { "user": userChoice, "account": accountChoice },
            success: result => {
                let roles = result.roles;
                for (let i = 0; i < roleTableBodyRows.length; i++) {
                    let checkbox = roleTableBodyRows[i].getElementsByTagName('input')[0];
                    if (roles.includes(checkbox.name))
                        checkbox.checked = true;
                }
                addCheckboxEventListeners();
            },
            error: err => {
                console.error(err);
            }
        })
    }
}

userInput.addEventListener('change', handleChange);
accountInput.addEventListener('change', handleChange);

$('#userRoleModal').on('hide.bs.modal', e => { 
    for (let i = 0; i < userInput.options.length; i++) {
        if (userInput.options[i].selected) userInput.options[i].selected = false;
    }

    for (let i = 0; i < accountInput.options.length; i++) {
        if (accountInput.options[i].selected) accountInput.options[i].selected = false;
    }
    resetCheckboxes();
    userChoice = undefined;
    accountChoice = undefined;
});

// var userId;

// $('#userRoleModal').on('show.bs.modal', e => {
//     let userDataset = e.relatedTarget.parentElement.parentElement.dataset;
//     userId = userDataset.id;

//     let url = "/advertising/admin/user/" + userId + "/roles"
//     $.ajax({
//         type: "GET",
//         url: url,
//         data: userId,
//         success: (result) => {
//             let roles = result.roles;
//             for (let i = 0; i < roleTableBodyRows.length; i++) {
//                 let checkbox = roleTableBodyRows[i].getElementsByTagName('input')[0];
//                 if (roles.includes(checkbox.name))
//                     checkbox.checked = true;
//             }
//             addCheckboxEventListeners();
//         },
//         error: err => {
//             console.error(err.statusText)
//             alert(err.statusText)
//             $('#userRoleModal').modal('hide');
//         }
//     })
// });

const addCheckboxEventListeners = () => {
    for (let i = 0; i < roleTableBodyRows.length; i++) {
        let checkbox = roleTableBodyRows[i].getElementsByTagName('input')[0];
        checkbox.addEventListener('click', saveUserRole)
    }
}

const saveUserRole = (e) => {
    let url = "/advertising/admin/user/" + userChoice + "/roles/save/";
    $.ajax({
        type: "POST",
        url: url,
        headers: {
            "X-CSRFTOKEN": getCookie('csrftoken')
        },
        data: { 
            "role": e.target.name, 
            "hasRole": e.target.checked,
            "account": accountChoice 
        },
        error: result => {
            console.error(result);
        }
    });
}

const resetCheckboxes = () => {
    for (let i = 0; i < roleTableBodyRows.length; i++) {
        let checkbox = roleTableBodyRows[i].getElementsByTagName('input')[0];
        checkbox.checked = false;
    }
}

const getCookie = name => {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}