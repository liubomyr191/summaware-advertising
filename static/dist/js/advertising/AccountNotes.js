console.log('AccountNotes.js');

const accountNotesInput = document.getElementById('account_notes');
const accountNotesSubmitBtn = document.getElementById('notes-submit-btn');

const salesRepInput = document.getElementById('sales_rep_notes');
const salesRepSubmitBtn = document.getElementById('sales-notes-submit-btn');

let accountNotesValue;
accountNotesInput.addEventListener('input', (e) => {
    accountNotesValue = e.target.value;
});

let salesRepNotesValue;
salesRepInput.addEventListener('input', (e) => {
    salesRepNotesValue = e.target.value;
    console.log(salesRepNotesValue);
});

accountNotesSubmitBtn.addEventListener('click', (e) => {
    e.preventDefault();
    if (accountNotesValue != '') {
        fetch(`/advertising/ajax/account/${account_id}/notes/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrf_token,
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "notes": accountNotesValue, "account_id": account_id }),

        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network issue');
            }
        }).then(json => {
            $('#account_notes').val('');
            $("#account-notes-modal").modal('hide');
            deleteAccountNotesTable();
            loadAccountNotes();
        }).catch(error => console.log(error.message));
    }
});

function loadAccountNotes() {
    fetch(`/advertising/ajax/account/${account_id}/notes/`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf_token,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            let notes = data.results;
            sortNotes(notes);
            let notesTableBody = document.getElementById('account-notes-table').getElementsByTagName('tbody')[0];
            notesTableBody.innerHTML = '';
            notes.forEach(note => {
                let row = document.createElement('tr');

                let timestampCell = document.createElement('td');
                let userCell = document.createElement('td');
                let noteCell = document.createElement('td');
                let editButtonCell = document.createElement('td');

                timestampCell.innerHTML = note.timestamp;
                userCell.innerHTML = note.user;
                noteCell.innerHTML = note.note;
                editButtonCell.innerHTML = `<button class="btn btn-sm btn-primary" data-toggle="modal" data-target="#edit-account-notes-modal" onclick="editAccountNote('${note.id}')">Edit</button>`;

                row.appendChild(timestampCell);
                row.appendChild(userCell);
                row.appendChild(noteCell);
                row.appendChild(editButtonCell);

                notesTableBody.appendChild(row);
            });
        })
}

function editAccountNote(id) {
    fetch(`/advertising/ajax/account/${account_id}/notes/${id}/`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf_token,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        let note = data.results;
        $('#edit-account-notes-modal-title').html(`Edit Note`);
        $('#edit-account-notes-modal-body').html(`<textarea id="edit-account-notes-textarea" cols="83" rows="3" class="form-control">${note.account_note.note}</textarea>`);
        $('#edit-account-notes-modal-footer').html(`<button class="btn btn-sm btn-primary" onclick="updateAccountNote('${note.account_note.id}')">Update</button>`);
    })
}

function updateAccountNote(note_id) {
    let note = $('#edit-account-notes-textarea').val();
    fetch(`/advertising/ajax/account/${account_id}/notes/${note_id}/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf_token,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "note_id": note_id,
            "note": note,
            "account_id": account_id
        })
    }).then(response => {
        if (response.ok) {
            $('#edit-account-notes-modal').modal('hide');
            loadAccountNotes();
        } else {
            throw new Error('Network issue');
        }
    }).catch(error => console.log(error.message));
}

function deleteAccountNotesTable() {
    let notesTableBody = document.getElementById('account-notes-table').getElementsByTagName('tbody')[0];
    for (let i = notesTableBody.rows.length - 1; i >= 0; i--) {
        notesTableBody.deleteRow(i);
    }
}

function deleteSalesRepNotesTable() {
    let notesTableBody = document.getElementById('sales-rep-notes-table').getElementsByTagName('tbody')[0];
    for (let i = notesTableBody.rows.length - 1; i >= 0; i--) {
        notesTableBody.deleteRow(i);
    }
}

function sortNotes(arr) {
    return arr.sort((a, b) => {
        return b.id - a.id;
    });
}

function loadSalesRepNotes() {
    fetch(`/advertising/ajax/account/${account_id}/salesrep/${sales_rep_id}/notes/`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf_token,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        let notes = data.results;
        sortNotes(notes);
        let notesTableBody = document.getElementById('sales-rep-notes-table').getElementsByTagName('tbody')[0];
        notesTableBody.innerHTML = '';
        notes.forEach(note => {
            let row = document.createElement('tr');

            let timestampCell = document.createElement('td');
            let userCell = document.createElement('td');
            let noteCell = document.createElement('td');
            let editButtonCell = document.createElement('td');

            timestampCell.innerHTML = note.timestamp;
            userCell.innerHTML = note.sales_person.first_name + ' ' + note.sales_person.last_name;
            noteCell.innerHTML = note.note;
            editButtonCell.innerHTML = `<button class="btn btn-sm btn-primary" data-toggle="modal" data-target="#edit-sales-rep-notes-modal" onclick="editSalesRepNote('${note.id}')">Edit</button>`;

            row.appendChild(timestampCell);
            row.appendChild(userCell);
            row.appendChild(noteCell);
            row.appendChild(editButtonCell);

            notesTableBody.appendChild(row);
        });
    })
}

function editSalesRepNote(id) {
    fetch(`/advertising/ajax/account/${account_id}/salesrep/${sales_rep_id}/notes/${id}/`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf_token,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        let note = data.results;
        $('#modal-title').html(`Edit Sales Rep Note for ${note.sales_person.first_name} ${note.sales_person.last_name}`);
        $('#modal-body').html(`<textarea id="sales-rep-notes-textarea" class="form-control" rows="3">${note.note}</textarea>`);
        $('#modal-footer').html(`<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                    <button class="btn btn-sm btn-primary" onclick="updateSalesRepNote('${note.id}')">Update</button>`);
    });
}

function updateSalesRepNote(note_id) {
    let salesRepNotesValue = $('#sales-rep-notes-textarea').val();
    if (salesRepNotesValue.length > 0) {
        fetch(`/advertising/ajax/account/${account_id}/salesrep/${sales_rep_id}/notes/${note_id}/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrf_token,
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                note_id: note_id,
                note: salesRepNotesValue,
                sales_rep_id: sales_rep_id,
                account_id: account_id
            })
        }).then(json => {
            $('#sales-rep-notes-textarea').val('');
            $("#edit-sales-rep-notes-modal").modal('hide');
            loadSalesRepNotes();
        }).catch(error => console.log(error.message));
    } else {
        alert('Please enter a note.');
    }
}



salesRepSubmitBtn.addEventListener('click', (e) => {
    console.log(JSON.stringify({ "notes": salesRepNotesValue, "account_id": account_id, "sales_rep_id": sales_rep_id }))
    e.preventDefault();
    if (salesRepNotesValue != '') {
        fetch(`/advertising/ajax/account/${account_id}/salesrep/${sales_rep_id}/notes/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrf_token,
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "notes": salesRepNotesValue, "account_id": account_id, "sales_rep_id": sales_rep_id }),

        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network issue');
            }
        }).then(json => {
            $('#sales_rep_notes').val('');
            $("#sales-rep-notes-modal").modal('hide');
            deleteSalesRepNotesTable();
            loadSalesRepNotes();
        }).catch(error => console.log(error.message));
    }
});

loadAccountNotes();
loadSalesRepNotes();