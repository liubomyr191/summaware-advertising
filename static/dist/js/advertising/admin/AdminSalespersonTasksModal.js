var salesrepId;
var taskList;
var taskId;
$('#salesrepModal').on('show.bs.modal', e => {
    var dataset = e.relatedTarget.parentElement.parentElement.dataset;
    salesrepId = dataset.id;

    const tasksTable = document.querySelector('#tasks-table');
    const tasksTableBody = tasksTable.getElementsByTagName('tbody')[0];

    $('#tasks-table tbody').empty();

    let url = `/advertising/ajax/${salesrepId}/tasks/`;
    $.ajax({
        type: "GET",
        url: url,
        success: result => {
            $('#salesrep-name').text(result.name);
            
            taskList = result.taskList ? result.taskList : [];
            if (taskList.length > 0) {
                populateTaskTable(taskList);
            } else {
                let tbody = $('#tasks-table tbody')[0];
                tbody.append('No tasks found.');
            }

        },
        error: error => {
            console.error(error.statusText)
        }
    });
});

$('#add-task-btn').click(e => {
    $('#new-task-modal').modal('show')
})

$('#new-task-submit-btn').click(e => {
    e.preventDefault();
    console.log('new-task-submit-btn clicked');
    let form = $('#new-task-form');
    let formData = new FormData(form[0]);

    let data = {};
    
    for (const [key, value] of formData) {
        data[key] = value;
    }

    data['salesrep_id'] = salesrepId;

    let url = `/advertising/ajax/tasks/new/`;
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => { return response.json(); })
    .then(data => {
        $('#new-task-modal').modal('hide');
        taskList.push(data.task);
        populateTaskTable(taskList)
    })
    .catch(err => console.error(err));
})

const populateTaskTable = (tasks) => {
    let currentDate = new Date().toJSON().slice(0, 10);
    console.log(currentDate)
    $('#tasks-table tbody').empty();
    taskRows = []
    tasks.forEach(task => {
        if (task.date < currentDate) {
            task.completed = false;
            taskRows.push(`<tr id="task-${task.id}" data-id="${task.id}">
                                <td><input type="checkbox" class="complete-checkbox"/></td>
                                <td>${task.date}</td>
                                <td style="color:red;">${task.text}</td>
                                <td>
                                    <button class="btn btn-danger delete-btn" data-toggle="modal" data-target="#delete-task-modal">
                                        <i class="fa fa-trash"></i> Delete
                                    </button>
                                </td>
                            </tr>`);
        } else {
            taskRows.push(`<tr id="task-${task.id}" data-id="${task.id}">
                        <td><input type="checkbox" class="complete-checkbox"/></td>
                        <td>${task.date}</td>
                        <td>${task.text}</td>
                        <td>
                            <button class="btn btn-danger delete-btn" data-toggle="modal" data-target="#delete-task-modal">
                                <i class="fa fa-trash"></i> Delete
                            </button>
                        </td>
                    </tr>`)
        }
    });
    $('#tasks-table tbody').append(taskRows);

    const completeCheckboxes = document.querySelectorAll('.complete-checkbox');
    completeCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('click', e => {
            let taskId = checkbox.parentElement.parentElement.dataset.id;
            markTaskComplete(taskId);
        })
    })

    const deleteBtns = document.querySelectorAll('.delete-btn');
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', e => {
            let rowDataset = e.target.parentElement.parentElement.dataset;
            taskId = rowDataset.id;
        })
    })
}

const confirmDeleteBtn = document.querySelector('#confirm-delete-btn');
confirmDeleteBtn.addEventListener('click', e => deleteTask(taskId))

const deleteTask = (taskId) => {
    let url = `/advertising/ajax/tasks/delete/`;
    let data = { "task": taskId, "salesrep_id": salesrepId }
    console.log(data)
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(res => {
        $('#delete-task-modal').modal('hide');
        taskList = taskList.filter(el => el.id != taskId)
        if (taskList.length > 0) {
            populateTaskTable(taskList);
        } else {
            let tbody = $('#tasks-table tbody')[0];
            tbody.innerHTML = '';
            tbody.append('No tasks found.');
        }
    })
    .catch(err => {
        console.error(err);
    })
}

const markTaskComplete = (id) => {
    let url = `/advertising/ajax/tasks/complete/`;
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "task": id,
            "salesrep_id": salesrepId 
        }),
    })
    .then(response => response.json())
    .then(res => {
        console.log(res);
        taskList = taskList.filter(el => el.id != id);
        populateTaskTable(taskList);
    })
    .catch(err => {
        console.error(err)
    });
}

$('#new-task-modal').on('hide.bs.modal', e => {
    $('input[name="text"]').val('');
    $('input[name="date"]').val('');
});