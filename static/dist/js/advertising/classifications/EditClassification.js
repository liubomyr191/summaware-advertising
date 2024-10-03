
function updateAdrate() {
    let id = document.getElementById("rate_id").value;
    let name = document.getElementById("name").value;
    let unit_type = document.getElementById("unit-type").value;
    let price_per_unit = document.getElementById("price-per-unit").value;
    let rate_type = document.getElementById("rate-type").value;
    let ad_location = document.getElementById("ad-location").value;
    let description = document.getElementById("description").value;
    let publication = document.getElementById("publication").value;
    let gl_code = document.getElementById("gl-code").value;
    let start_date = document.getElementById("start-date").value;
    let end_date = document.getElementById("end-date").value;
    let pricing =  document.getElementById("pricing").value;
    let tax_category =  document.getElementById("tax-category").value;
    let locked = document.getElementById("locked").checked;
    let status = document.getElementById("status").value;
    let hidden = document.getElementById("hidden").value;

    if(name === "") {
        $.toastr.warning("Please enter Ad name"); return;
        
    }   

    if(unit_type === "0") {
        $.toastr.warning("Please select unit type"); return;
    }

    if(price_per_unit === "") {
        $.toastr.warning("Please enter Price Per Unit"); return;
    }

    if(rate_type === "0") {
        $.toastr.warning("Please select Ract type"); return;
    }

    if(ad_location === "") {
        $.toastr.warning("Please enter Ad location"); return;
    }

    if(description === "") {
        $.toastr.warning("Please enter Ad description"); return;
    }

    if(publication === "0") {
        $.toastr.warning("Please select Ad publication"); return;
    }

    if(gl_code === "0") {
        $.toastr.warning("Please select Ad gl code"); return;
    }

    if(start_date === "") {
        $.toastr.warning("Please select start date"); return;
    }

    if(end_date === "") {
        $.toastr.warning("Please select end date"); return;
    }

    if(pricing === "0") {
        $.toastr.warning("Please select pricing"); return;
    }

    if(tax_category === "0") {
        $.toastr.warning("Please select tax category"); return;
    }

    let atlocked = "";

    if(locked === true) {
        atlocked = 1;
    }

    else atlocked = 0;

    let data = {
        id : id,
        name : name,
        description : description,
        location : ad_location,
        unit_type : unit_type,
        unit_price : price_per_unit,
        tax_category : tax_category,
        ad_type_id : rate_type,
        start_date : start_date,
        end_date : end_date,
        locked : atlocked,
        pricing : pricing,
        default_gl_code_id : gl_code,
        pbulication_id : publication,
        status : status,
        hidden : hidden,
    }

    console.log(data)

    fetch('/advertising/classifieds/rates/edit/', {
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
        $.toastr.success('Saved Success');
    })
    .catch(error => {
        $.toastr.error("Saved failure");
    });
}

const getCookie = name => {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}