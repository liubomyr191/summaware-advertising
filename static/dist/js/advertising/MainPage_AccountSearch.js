var searchInput = document.getElementById('search');
var table = document.getElementById('resultsTable');
var tBody = table.tBodies[0];
var rows = tBody[0];

searchInput.addEventListener('keyup', function () {
    var searchValue = searchInput.value;

    if (searchValue == '') {
        console.log('empty');
    }

    fetch(`/advertising/ajax/search/account/?value=${searchValue}`, {
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
        if (data.length == 0) {
            table.innerHTML = 'No results found';
        } else {
            // create a table row for each result
            var results = data.results
            var rows = '';
            for (var i = 0; i < results.length; i++) {

                // loop through publications and create a row for each
                if (results[i].publications.length > 0) {
                    var publications = results[i].publications;
                    for (var j = 0; j < publications.length; j++) {
                        if (publications[j].account == results[i].id) {
                            rows += `<tr>
                                        <td>${publications[j].id}</td>
                                        <td><a href='/advertising/publication/${publications[j].id}'>${publications[j].name}</a></td>
                                        <td>${results[i].id}</td>
                                        <td><a href='/advertising/account/${results[i].id}'>${results[i].name}</a></td>
                                        <td>${results[i].account_type.name}</td>
                                    </tr>`;
                        }
                    }
                } else {
                    rows += `<tr>
                                <td></td>
                                <td></td>
                                <td>${results[i].id}</td>
                                <td><a href='/advertising/account/${results[i].id}'>${results[i].name}</a></td>
                                <td>${results[i].account_type.name}</td>
                                
                            </tr>`;
                }
            }
            tBody.innerHTML = rows;
        }
    });
});