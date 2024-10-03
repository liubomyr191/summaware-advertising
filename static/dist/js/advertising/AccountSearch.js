const accountInput = document.getElementById('account');

accountInput.addEventListener('keyup', function () {
    var searchValue = accountInput.value;
    if (searchValue.length == 0) {
        document.getElementById('accountDropdown').style.display = 'none';
        return;
    }
    fetch(`/advertising/ajax/order/search/account/?value=${searchValue}`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) return response.json();
    }).then(data => {
        let results = data.results;
        var dropdown = document.getElementById('accountDropdown');
        dropdown.style.display = 'block';
        var options = '';
        for (var i = 0; i < results.length; i++) {
            options += `<li data-id='${results[i].id}' class='dropdown-item'
                            value='${results[i].id}' 
                            style='list-style-type: none;'>
                                ${results[i].name}
                        </li>`;
        }
        dropdown.innerHTML = options;

        var dropdownItems = document.getElementsByClassName('dropdown-item');
        for (var i = 0; i < dropdownItems.length; i++) {
            dropdownItems[i].addEventListener('click', function () {
                accountInput.value = this.textContent.trim();
                document.getElementById('accountDropdown').style.display = 'none';
                fetch(`/advertising/ajax/order/search/publication/?value=${accountInput.value}`, {
                    method: "GET",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": "{{ csrf_token }}",
                        "Accept": "application/json",
                        'Content-Type': 'application/json'
                    }
                }).then(response => {
                    if (response.ok) return response.json();
                }
                ).then(data => {
                    for (var i = 0; i < data.results.length; i++) {
                        options += `<option value='${data.results[i].id}'>${data.results[i].name}</option>`;
                    }
                    document.getElementById('publication').innerHTML = options;
                });
            });
        }
    });
});