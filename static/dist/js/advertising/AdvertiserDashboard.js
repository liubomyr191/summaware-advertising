let typeItems = document.querySelectorAll(".advertiser-type-item");
let advertiser_new_address=document.getElementById("advertiser_new_address");
let advertiser_same_address=document.getElementById("advertiser_same_address");
let bilAddressEle = document.getElementById("billing-address");
let bilCityEle = document.getElementById("billing-city");
let bilStateEle = document.getElementById("billing-state");
let bilZipCodeEle = document.getElementById("billing-zip-code");

let contactSectionEle = document.getElementById("contact-section");
let addBtnEle = document.getElementById("add-company");
let companyInfoEle = document.getElementById("company-info");
let companyBackImg = document.getElementById("company-backImg");
let companyStar = document.getElementById("company-star");

let overviewMenu = document.getElementById("id_advertiser_overview");
let activityMenu = document.getElementById("id_overview_activity");
let historyMenu = document.getElementById("id_order_history");

let overviewTab = document.getElementById("id_overview_tab");
let activityTab = document.getElementById("id_activity_tab");
let historyTab = document.getElementById("id_order_history_tab");

let activeToggle = document.getElementById("id_to_active");
let completeToggle = document.getElementById("id_to_complete");

let activityTime = document.getElementById("id_activity_time");
let activityProduct = document.getElementById("id_activity_product");
let activityFormat = document.getElementById("id_activity_format");

let historyFilterPolygon = document.getElementById("id_history_filter_polygon");
let historyFilter = document.getElementById("id_history_filter");
let filterFlag = false;

let mainStatusContent = document.getElementById("main_status_content");
let mainStatus = document.getElementById("main_status");
let mainAddress = document.getElementById("main_address");
let mainWebsite = document.getElementById("main_website");
let mainAccountTypeId = document.getElementById("main_account_type_id");
let mainPhone = document.getElementById("main_phone");
let mainEmail = document.getElementById("main_email");

let billRecTotal = document.getElementById("bill_rec_total");
let billAddress = document.getElementById("bill_address");
let billCreditLimit = document.getElementById("bill_credit_limit");
let billEmail = document.getElementById("bill_email");

let addressFlag = 0;
let mainSearchFlag = false;
let mainFilterFlag = false;

$(function () {
    let data = {}
    data = {
        'param': 'all',

    }
    search_filter_result(data)
});

function changeAddress(index) {
    addressFlag = index;

    Array.from(typeItems).forEach(typeItem => {
        typeItem.classList.remove('selected-radio');
    })

    document.getElementById("address-" + index).classList.add("selected-radio");

    if (index == 0) {
        document.getElementById("advertiser_new_address").style.display = 'block'
        document.getElementById("advertiser_same_address").style.display = 'none'
        bilAddressEle.disabled = false;
        bilCityEle.disabled = false;
        bilStateEle.disabled = false;
        bilZipCodeEle.disabled = false;
    } else {
        document.getElementById("advertiser_new_address").style.display = 'none'
        document.getElementById("advertiser_same_address").style.display = 'block'
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
$('#id_edit_info').click(e => {
    $('#modal-info').modal('show')
})

function selSearch() {
    mainSearchFlag = !mainSearchFlag

    contactSectionEle.classList.remove('filter-active');

    if (mainSearchFlag)
        contactSectionEle.classList.add('search-active');
    else
        contactSectionEle.classList.remove('search-active');
}

var input = document.getElementById("id_search_contacts");


// Add a keypress event listener to the input
$("#id_search_contacts").keypress(function (event) {
    console.log("hello");
    // Check if the key pressed is the "Enter" key
    if (event.which === 13) {
        // Call a function or perform an action when the "Enter" key is pressed
        var search_val = $('#id_search_contacts').val();
        let data = {}
        data = {
            'param': 'search',
            'search_val': search_val
        }
        search_filter_result(data)
    }
});

function search_filter_result(data) {
    fetch('/advertising/search_filter_contacts/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            showData(data);

            document.getElementById("id_contact_count").innerText = Number(data['active'].length) + Number(data['inactive'].length);
        })
        .catch(error => {
            // console.log(error);
            $.toastr.error("Saved failure");
        });
}

function search_contacts() {
    var search_val = $('#id_search_contacts').val();
    let data = {}
    data = {
        'param': 'search',
        'search_val': search_val
    }

    search_filter_result(data)
}

function filterContacts() {
    var filter_status = $('#id_filter_status').val();
    var filter_dept = $('#id_filter_dept').val();
    let data = {}
    data = {
        'param': 'filter',
        'status': Number(filter_status),
        'dept': Number(filter_dept),
    }
    console.log(data)
    search_filter_result(data)
}

function editWalmartInfo(param) {
    let data = {}
    if (param == 'walmart') {
        if (document.getElementById('id_walmart_account').value == 0) {
            $.toastr.warning("Please select accountType");
            return;
        }

        data = {
            id: advertiserId,
            param: param,
            accountType: document.getElementById('id_walmart_account').value,
            address: document.getElementById('id_walmart_address').value,
            status: document.getElementById('id_walmart_status_type').value,
            phone: document.getElementById('id_walmart_phone').value,
            email: document.getElementById('id_walmart_email').value,
            website: document.getElementById('id_walmart_website').value
        }
    }
    if (param == 'billing') {
        data = {
            id: advertiserId,
            param: param,
            billing_total_spent: document.getElementById('id_billing_total').value,
            billing_address: document.getElementById('id_billing_address').value,
            credit_limit: document.getElementById('id_credit_limit').value,
            billing_email: document.getElementById('id_billing_email').value,
        }
    }

    fetch('/advertising/edit_new_advertiser/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            let tempData = data['data'];
            $.toastr.success('Updated Success');

            if (tempData['param'] === "walmart") {
                $('#overview-walmart').modal('hide');

                mainStatusContent.innerText = tempData['status'] == 0 ? "Active" : "InActive";
                mainStatus.value = tempData['status'];
                mainAddress.innerText = tempData['address'];
                mainWebsite.innerText = tempData['website'];
                mainAccountTypeId.innerText = tempData['accountType'];
                mainPhone.innerText = tempData['phone'];
                mainEmail.innerText = tempData['email'];

                for (let i = 0; i < accountTypeList.length; i ++) {
                    if (accountTypeList[i]['pk'] == tempData['accountType']) {
                        mainAccountType.innerText = accountTypeList[i]['fields']['name'];
                    }
                }
            } else {
                $('#overview-billing').modal('hide');

                billRecTotal.innerText = tempData['billing_total_spent'];
                billAddress.innerText = tempData['billing_address'];
                billCreditLimit.innerText = tempData['credit_limit'];
                billEmail.innerText = tempData['billing_email'];
            }
        })
        .catch(error => {
            $.toastr.error("Saved failure");
        });
}

function selFilter() {
    filterFlag = !filterFlag;

    contactSectionEle.classList.remove('search-active');

    if (filterFlag)
        contactSectionEle.classList.add('filter-active');
    else
        contactSectionEle.classList.remove('filter-active');
}

function addCompany() {
    addBtnEle.style.display = "none";
    companyBackImg.style.display = "none";
    companyInfoEle.style.opacity = "1";

    contactSectionEle.classList.remove("search-active");
    contactSectionEle.classList.remove("filter-active");

    document.getElementById("i-company-item-id").value = 0
    document.getElementById("i-first-name").value = "";
    document.getElementById("i-last-name").value = "";
    document.getElementById("i-email").value = "";
    document.getElementById("i-department").value = "";
    document.getElementById("i-phone-number").value = "";
}

function deleteCompanyContact(id) {
    let isConfirmed = confirm('Are you sure you want to remove?');
    if (!isConfirmed) return;
    let data = {}
    data = {
        'id': id,
    }
    fetch('/advertising/delete_id_contact/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            $.toastr.success('Changed InActive');
            showData(data)
        })
        .catch(error => {
            $.toastr.error("Saved failure");
        });
}

function editCompanyContact(id) {
    addCompany();

    let full_name = document.getElementById('first-name-' + id).innerHTML
    let nameParts = full_name.split(" ");
    let firstName = nameParts[0] ? nameParts[0] : "";
    let lastName = nameParts[1] ? nameParts[1] : "";
    
    document.getElementById("i-company-item-id").value = id
    document.getElementById("i-first-name").value = firstName
    document.getElementById("i-last-name").value = lastName
    document.getElementById("i-email").value = document.getElementById('email-' + id).innerHTML;
    document.getElementById("i-department").value = document.getElementById('department-' + id).innerHTML;
    document.getElementById("i-phone-number").value = document.getElementById('phone-' + id).innerHTML ? document.getElementById('phone-' + id).innerHTML : "";
}

function cancelContact() {
    companyInfoEle.style.opacity = "0";
    addBtnEle.style.display = "block";
    companyBackImg.style.display = "block";
}

function createContact(id) {
    if (document.getElementById('i-department').value == 0) {
        $.toastr.warning("Please select Department");
        return;
    }
    if (document.getElementById('i-first-name').value == '' ||
        document.getElementById('i-last-name').value == '' ||
        document.getElementById('i-email').value == '' ||
        document.getElementById('i-phone-number').value == ''
        ) {
        $.toastr.warning("Please Input Value Correctly");
        return;
    }

    data = {
        'id': Number(document.getElementById("i-company-item-id").value),
        'account': Number(id),
        'firstname': $('#i-first-name').val(),
        'lastname': $('#i-last-name').val(),
        'full_name': $('#i-first-name').val() + $('#i-last-name').val(),
        'email': $('#i-email').val(),
        'department': Number($('#i-department').val()),
        'phone': $('#i-phone-number').val(),
        'default': companyStar.classList.contains("sel-star") ? 1 : 0
    }
    fetch('/advertising/create_contact/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            $.toastr.success('Save Success');
            showData(data);

            document.getElementById("id_contact_count").innerText = Number(data['active'].length) + Number(data['inactive'].length);
        })
        .catch(error => {
            $.toastr.error("Saved failure");
        });
}

function selStar() {
    if (companyStar.classList.contains("sel-star")) {
        companyStar.classList.remove("sel-star");
    } else {
        companyStar.classList.add("sel-star");
    }
}

function activateTab(type) {
    overviewMenu.classList.remove('overview-active');
    activityMenu.classList.remove('overview-active');
    historyMenu.classList.remove('overview-active');

    overviewTab.classList.add('disable-tab');
    activityTab.classList.add('disable-tab');
    historyTab.classList.add('disable-tab');

    if (type === 0) {
        overviewMenu.classList.add('overview-active');
        overviewTab.classList.remove('disable-tab');
        let data = {}
        data = {
            'param': 'all',
        }
        search_filter_result(data)

    } else if (type === 1) {
        showActivity()
        activityMenu.classList.add('overview-active');
        activityTab.classList.remove('disable-tab');
    } else {
        historyMenu.classList.add('overview-active');
        historyTab.classList.remove('disable-tab');
    }
}

function showActivity() {
    showTaskList("active")
}

function showTaskList(param) {
    let data = {
        'status': param
    }
    fetch('/advertising/getTaskList/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            TaskList(data)

        })
        .catch(error => {
            $.toastr.error("Saved failure");
        });

}

function TaskList(data) {
    $('#id_todo_task_list').empty();
    if (data['active'].length > 0) {
        for (var i = 0; i < data['active'].length; i++) {
            let tempData = data['active'][i];
            $('#id_todo_task_list').append(`
                <div class="task-info-item">
                    <div class="task-info">
                        <div class="task-info-header">
                            <div class="task-info-header-title" id="id_task_${tempData['id']}">${tempData['title']}</div>

                            <div class="task-info-header-date">Due: <span id="id_task_due_${tempData['id']}">${tempData['due_date']}</span></div>
                        </div>

                        <div class="task-info-content" id="id_task_content_${tempData['id']}">
                            ${tempData['content']}
                        </div>

                        <div class="task-info-footer">
                            <div class="task-info-level">Priority Lvl: <span id="id_task_priority_${tempData['id']}">${tempData['priority']}</span></div>

                            <div class="task-info-assign">Assigned To: <span  id="id_task_account_${tempData['id']}">${tempData['account_id']}</span></div>
                        </div>
                    </div>

                    <div class="task-option">
                        <div class="task-edit" data-target="#new-task" data-toggle="modal"><i class="fa fa-pencil" onclick="editTaskActivity(${tempData['id']})"></i></div>

                        <div class="task-check" onclick="completeTask(${tempData['id']})"><i class="fa fa-check" style="color: black"></i></div>

                        <div class="task-trash" onclick="deleteTask(${tempData['id']})"><i class="fa fa-trash"></i></div>
                    </div>
                </div>
            `);
        }
    } else {
        $('#id_todo_task_list').append(`
            <div class="contacts-inactive">
                <div class="contacts-inactive-no">
                    There is no TO DO's
                </div>
            </div>`)
    }
}

function editTaskActivity(id) {
    document.getElementById("id_task_hidden").value = id;
    document.getElementById("id_task_title").value = document.getElementById('id_task_' + id).innerText;
    document.getElementById("id_task_due_date").value = document.getElementById('id_task_due_' + id).innerText;
    document.getElementById("id_task_priority").value = document.getElementById('id_task_priority_' + id).innerText;
    document.getElementById("id_task_content").value = document.getElementById('id_task_content_' + id).innerText;
    document.getElementById("id_assign").value = document.getElementById('id_task_account_' + id).innerText;
}

function toogle(type) {
    activeToggle.classList.remove('toogle-active');
    completeToggle.classList.remove('toogle-active');

    if (type === 0) {
        showTaskList('active')
        activeToggle.classList.add('toogle-active');
    } else {
        showTaskList('complete')
        completeToggle.classList.add('toogle-active');
    }
}

function deleteTask(id) {
    let isConfirmed = confirm('Are you sure you want to remove?');
    if (!isConfirmed) return;

    let data = {'id': id,};

    fetch('/advertising/taskRemove/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        $.toastr.success('Deleted Task');

        TaskList(data)
    })
    .catch(error => {
        $.toastr.error("Saved failure");
    });
}

function selSalesTab(type) {
    activityTime.classList.remove('activity-active');
    activityProduct.classList.remove('activity-active');
    activityFormat.classList.remove('activity-active');

    if (type === 0) {
        activityTime.classList.add('activity-active');
    } else if (type === 1) {
        activityProduct.classList.add('activity-active');
    } else {
        activityFormat.classList.add('activity-active');
    }
}

function completeTask(id) {
    let data = {'id': id};

    fetch('/advertising/taskSetActivity/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            $.toastr.success('Completed Task');

            TaskList(data)
        })
        .catch(error => {
            $.toastr.error("Saved failure");
        });
}

function showData(data) {
    $('#id_active_items').empty();
    $('#id_inactive_items').empty();
    if (data['active'].length > 0) {
        for (var i = 0; i < data['active'].length; i++) {

            let starEle = "";
            if (data['active'][i]['default'] == 1)
                starEle = `<i class="fa fa-star"></i>`;

            $('#id_active_items').append(`
                <div class="contacts-left-active-item ">
                    <div class="contacts-left-first">
                        ${i + 1}
                    </div>
                    
                    <input id="active-id" type="hidden" value="${data['active'][i]['id']}">
                    
                    <div class="contacts-left-second">
                        <div class="contacts-left-second-one">
                            <div class="contact-name-section">
                                <span id="first-name-${data['active'][i]['id']}" class="contact-name">${data['active'][i]['full_name']}</span>
                            </div>
                            -<span id="department-${data['active'][i]['id']}" style="font-size: 14px">${data['active'][i]['department_id']}</span>
                            ` + starEle + `
                        </div>
                        
                        <div class="contacts-left-second-two">
                            <div class="contacts-left-second-two-a">
                                <div style=""><i class="fa fa-phone font-s-1" style=""></i>Phone
                                </div>
                                <div id="phone-${data['active'][i]['id']}" class="company-data">${data['active'][i]['phone_number']}</div>
                            </div>
                            
                            <div class="contacts-left-second-two-a">
                                <div><i class="fa fa-envelope-o font-s-1"></i>Email</div>
                                <div id="email-${data['active'][i]['id']}" class="company-data">${data['active'][i]['email']}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contacts-left-third">
                        <i class="fa fa-pencil midi-icon" onClick="editCompanyContact(${data['active'][i]['id']})"></i>
                        <i class="fa fa-trash midi-icon" onClick="deleteCompanyContact(${data['active'][i]['id']})"></i>
                    </div>
                </div>
            `);
        }
    } else {
        $('#id_active_items').append(
            `<div class="contacts-inactive">
                <div class="contacts-inactive-no">
                    There are currently no inactive company contacts
                </div>
            </div>`);
    }

    if (data['inactive'].length > 0) {
        for (var i = 0; i < data['inactive'].length; i++) {
            let inStarEle = "";
            if (data['inactive'][i]['default'] == 1)
                inStarEle = `<i class="fa fa-star"></i>`;

            $('#id_inactive_items').append(`
                <div class="contacts-left-active-item ">
                    <div class="contacts-left-first">
                    ${i + 1}
                    </div>
                    
                    <input id="inactive-id" type="hidden" value="${data['inactive'][i]['id']}">

                    <div class="contacts-left-second">
                        <div class="contacts-left-second-one">
                            <div class="contact-name-section">
                                <span id="first-name-${data['inactive'][i]['id']}" class="contact-name">${data['inactive'][i]['full_name']}</span>
                            </div>
                            -<span id="department-${data['inactive'][i]['id']}" style="font-size: 14px">${data['inactive'][i]['department']}</span>
                            ` + inStarEle + `
                        </div>
                        
                        <div class="contacts-left-second-two">
                            <div class="contacts-left-second-two-a">
                                <div style=""><i class="fa fa-phone font-s-1" style=""></i>Phone
                                </div>
                                <div id="phone-${data['inactive'][i]['id']}" class="company-data">${data['inactive'][i]['phone']}</div>
                            </div>
                            
                            <div class="contacts-left-second-two-a">
                                <div><i class="fa fa-envelope-o font-s-1"></i>Email</div>
                                <div id="email-${data['inactive'][i]['id']}" class="company-data">${data['inactive'][i]['email']}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contacts-left-third">
                        <i class="fa fa-pencil midi-icon" onClick="editCompanyContact(${data['inactive'][i]['id']})"></i>
                    </div>
                </div>
            `);
        }
    } else {
        $('#id_inactive_items').append(
            `<div class="contacts-inactive">
                        <div class="contacts-inactive-no">
                            There are currently no inactive company contacts
                        </div>
                    </div>`);
    }
}

function createTask() {
    if (document.getElementById('id_assign').value === 0) {
        $.toastr.warning("Please select Assign");
        return;
    }

    if (document.getElementById('id_task_title').value === '' ||
        document.getElementById('id_task_due_date').value === '' ||
        document.getElementById('id_task_priority').value === '' ||
        document.getElementById('id_task_content').value ==='')
    {
        $.toastr.warning("Please Input Value Correctly");
        return;
    }

    data = {
        'id': Number($('#id_task_hidden').val()),
        'title': $('#id_task_title').val(),
        'content': $('#id_task_content').val(),
        'due_date': $('#id_task_due_date').val(),
        'priority': $('#id_task_priority').val(),
        'account_id': Number($('#id_assign').val()),
        'note': $('#id_task_note').val(),
    }

    fetch('/advertising/create_task/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            $.toastr.success('Created Success');
            TaskList(data);
            $('#new-task').modal('hide');
        })
        .catch(error => {
            $.toastr.error("Saved failure");
        });
}

function initialTaskModal() {
    document.getElementById("id_task_hidden").value = "";
    document.getElementById("id_task_title").value = "";
    document.getElementById("id_task_due_date").value = "";
    document.getElementById("id_task_priority").value = "";
    document.getElementById("id_task_content").value = "";
    document.getElementById("id_assign").value = "";
}

function clickHistoryFilter() {
    filterFlag = !filterFlag;

    if (filterFlag) {
        historyFilterPolygon.classList.remove('disable-tab');
        historyFilter.classList.remove('disable-tab');
    } else {
        historyFilterPolygon.classList.add('disable-tab');
        historyFilter.classList.add('disable-tab');
    }
}

function setMainModal() {
    document.getElementById("id_walmart_status_type").value = mainStatus.value;
    document.getElementById("id_walmart_address").value = mainAddress.innerText;
    document.getElementById("id_walmart_website").value = mainWebsite.innerText;
    document.getElementById("id_walmart_account").value = mainAccountTypeId.value;
    document.getElementById("id_walmart_phone").value = mainPhone.innerText;
    document.getElementById("id_walmart_email").value = mainEmail.innerText;
}

function setBillingModal() {
    document.getElementById("id_billing_total").value = billRecTotal.innerText;
    document.getElementById("id_billing_address").value = billAddress.innerText;
    document.getElementById("id_credit_limit").value = billCreditLimit.innerText;
    document.getElementById("id_billing_email").value = billEmail.innerText;
}