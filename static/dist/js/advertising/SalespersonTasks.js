const tasksTable = document.querySelector('#salesrep-tasks-table');
const tasksTableBody = tasksTable.getElementsByTagName('tbody')[0];
const tasksTableBodyRows = tasksTableBody.rows;

const newTaskModal = document.querySelector('#new-task-modal');
const newTaskBtn = document.querySelector('#new-task-btn');
const textInput = document.querySelector('input[name="text"]');
const newTaskSubmitBtn = document.querySelector('#new-task-submit-btn');

const completeCheckboxes = document.querySelectorAll('.complete-checkboxes');

var taskId;
if (tasksTableBodyRows.length > 0) {
    const deleteBtns = document.querySelectorAll('.delete-btn');

    deleteBtns.forEach(btn => {
        btn.addEventListener('click', e => {
            let rowDataset = e.target.parentElement.parentElement.dataset;
            taskId = rowDataset.id;
        })
    })
    
    const confirmDeleteBtn = document.querySelector('#confirm-delete-btn');
    confirmDeleteBtn.addEventListener('click', e => {
        deleteTask(taskId)
    })
}

var textInputValue = '';
textInput.addEventListener('input', e => {
    textInputValue = e.target.value;
})

newTaskSubmitBtn.addEventListener('click', e => {
    e.preventDefault();

    if (textInputValue == '' ) {
        alert('New tasks need a text. Please try again.')
    }

    let url = `/advertising/ajax/tasks/new/`;
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "text": textInputValue,
            "salesrep_id": salesperson_id 
        }),
    })
    .then(response => response.json())
    .then(res => {
        console.log(res);
        window.location.reload();
    })
    .catch(err => console.error(err));
})

completeCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('click', e => {
        let taskId = checkbox.parentElement.parentElement.dataset.id;
        markTaskComplete(taskId);
    })
})

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
            "salesrep_id": salesperson_id 
        }),
    })
    .then(response => response.json())
    .then(res => {
        console.log(res);
        window.location.reload();
    })
    .catch(err => {
        console.error(err)
    });
}

const deleteTask = (taskId) => {
    let url = `/advertising/ajax/tasks/delete/`;
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "task": taskId,
            "salesrep_id": salesperson_id 
        }),
    })
    .then(response => response.json())
    .then(res => {
        console.log(res);
        window.location.reload();
    })
    .catch(err => {
        console.error(err);
    })
}