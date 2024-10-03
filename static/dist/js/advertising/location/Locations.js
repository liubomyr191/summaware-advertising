const createLocationModal = document.querySelector('#create_location_modal');
const createLocationForm = document.querySelector('#create_location_form');
const createLocationCode = document.querySelector('#locationCode');
const createDescription = document.querySelector('#description');
const createPC = document.querySelector('#PC');
const createSubmitBtn = document.querySelector('#create_location_submit');

const editBtns = document.querySelectorAll('.edit-btn');

const editLocationModal = document.querySelector('#edit_location_modal');
const editLocationForm = document.querySelector('#create_location_form');
const editLocationCode = document.querySelector('#editLocationCode');
const editDescription = document.querySelector('#editDescription');
const editPC = document.querySelector('#editPC');
const editSubmitBtn = document.querySelector('#edit_location_submit');

let locationId;


createSubmitBtn.addEventListener('click', e => {
    e.preventDefault();


    let locationCode = createLocationCode.value.replace(/\D/g, '');
    let pc = createPC.value.replace(/\D/g, '');

    if(locationCode.length < 1 || locationCode.length > 3)  {
        alert("Location Code length should be 3");
        return;
    }
    if(createDescription.value.length < 1 )  {
        alert("Please input the description!");
        return;
    }

    if(pc.length < 1 || pc.length > 2)  {    
        alert("PC length should be 2")
        return;
    }

    fetch(`/advertising/location/new/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        // send only numerical gl code
        body: JSON.stringify({
            location: createLocationCode.value,
            description: createDescription.value,
            pc : createPC.value
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#create_location_modal').modal('hide');
                window.location.reload();
            }
        })
        .catch(err => console.error(err))
});

$('#create_location_modal').on('hide.bs.modal', e => {
    createLocationCode.value = '';
    createDescription.value = '';
    createPC.value = '';
});

editBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        locationId = e.target.parentElement.parentElement.dataset.locationId
        $('#edit_location_modal').modal('show');
    })
})

$('#edit_location_modal').on('show.bs.modal', e => {
    console.log('editModal')
    if (locationId) {
        fetch(`/advertising/location/${locationId}/`, {
            method: 'GET'
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);

                let res = data.res;

                // Display the formatted code
                editLocationCode.value = res.location;
                editDescription.value = res.description;
                editPC.value = res.pc;
            })
    }
});

editSubmitBtn.addEventListener('click', e => {

    let locationCode = editLocationCode.value.replace(/\D/g, '');
    let pc = editPC.value.replace(/\D/g, '');

    if(locationCode.length < 1 || locationCode.length > 3)  {
        alert("Location Code length should be 3");
        return;
    }
    if(editDescription.value.length < 1 )  {
        alert("Please input the description!");
        return;
    }

    if(pc.length < 1 || pc.length > 2)  {    
        alert("PC length should be 2")
        return;
    }

    
    fetch(`/advertising/location/${locationId}/edit/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            location: editLocationCode.value,
            description: editDescription.value,
            pc : editPC.value
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            if (data.message.includes('Error.')) {
                alert(data.message);
                return;
            } else {
                $('#edit_location_modal').modal('hide');
                window.location.reload();
            }
        })
        .catch(err => console.error(err))
})

const searchInput = document.querySelector('#search-location');
const searchTableBody = document.querySelector('#location_table_tbody');
const searchTableRows = searchTableBody.querySelectorAll('tr');
searchInput.addEventListener('keyup', () => {
    const searchValue = searchInput.value;
    searchCodes(searchValue)
});

const searchCodes = (searchValue) => {
    searchTableRows.forEach(row => {
        const rowTitle = row.querySelector('td:nth-child(2)').innerText;
        const rowCode = row.querySelector('td:nth-child(3)').innerText;

        if (searchValue === "") {
            row.style.display = '';
        } else if (!rowTitle.toLowerCase().includes(searchValue.toLowerCase()) && !rowCode.toLowerCase().includes(searchValue.toLowerCase()))
            row.style.display = 'none';
    });
}


function formatLocation(inputElement) {
    let formatted = inputElement.value.replace(/\D/g, ''); // Remove non-numeric characters
    inputElement.value = formatted;
}

// Attach event listeners to input elements
createLocationCode.addEventListener('input', () => {
    formatLocation(createLocationCode);
});
createPC.addEventListener('input', () => {
    formatLocation(createPC);
});

editLocationCode.addEventListener('input', () => {
    formatLocation(editLocationCode);
});

editPC.addEventListener('input', () => {
    formatLocation(editPC);
});


