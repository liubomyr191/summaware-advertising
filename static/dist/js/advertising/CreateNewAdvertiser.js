let typeItems = document.querySelectorAll(".advertiser-type-item");
let advertiser_new_address=document.getElementById("advertiser_new_address");
let advertiser_same_address=document.getElementById("advertiser_same_address");
let bilAddressEle = document.getElementById("billing-address");
let bilCityEle = document.getElementById("billing-city");
let bilStateEle = document.getElementById("billing-state");
let bilZipCodeEle = document.getElementById("billing-zip-code");

let addressFlag = 0;

function createAdvertiser() {
    let accountType = parseInt(document.getElementById("account-type").value);
    let firstName = document.getElementById("contact_name_first-name").value;
    let lastName = document.getElementById("contact_name_last-name").value;
    let businessName = document.getElementById("business-name").value;
    let address = document.getElementById("address").value;
    let city = document.getElementById("city").value;
    let state = document.getElementById("state").value;
    let zipCode = document.getElementById("zip-code").value;
    let phoneNumber = document.getElementById("phone-number").value;
    let email = document.getElementById("email").value;
    let website = document.getElementById("website").value;
    let marketCode = parseInt(document.getElementById("market-code").value);
    let salesPerson = parseInt(document.getElementById("sales-person").value);
    let submitter = document.getElementById("submitter").value;
    let legacyId = document.getElementById("legacy-id").value;
    let bilEmail = document.getElementById("billing-email").value;
    let bilAddress = document.getElementById("billing-address").value;
    let bilCity = document.getElementById("billing-city").value;
    let bilState = document.getElementById("billing-state").value;
    let bilZipCode = document.getElementById("billing-zip-code").value;

    if (accountType === 0) {
        $.toastr.warning("Please select account type"); return;
    }

    if (firstName === "") {
        $.toastr.warning("please enter first name"); return;
    }

    if (lastName === "") {
        $.toastr.warning("please enter last name"); return;
    }

    if (businessName === "") {
        $.toastr.warning("please enter business name"); return;
    }

    if (address === "") {
        $.toastr.warning("please enter address"); return;
    }

    if (city === "") {
        $.toastr.warning("please enter city"); return;
    }

    if (state === "") {
        $.toastr.warning("please select state"); return;
    }

    if (zipCode === "") {
        $.toastr.warning("please enter zip code"); return;
    }

    if (phoneNumber === "") {
        $.toastr.warning("please enter phone number"); return;
    }

    if (email === "") {
        $.toastr.warning("please enter email"); return;
    }

    if (website === "") {
        $.toastr.warning("please enter website"); return;
    }

    if (marketCode === 0) {
        $.toastr.warning("please enter market code"); return;
    }

    if (salesPerson === 0) {
        $.toastr.warning("please enter sales person"); return;
    }

    if (submitter === "") {
        $.toastr.warning("please enter submitter"); return;
    }

    if (legacyId === "") {
        $.toastr.warning("please enter legacy id"); return;
    }

    if (bilEmail === "") {
        $.toastr.warning("please enter billing email"); return;
    }

    if (bilAddress === "") {
        $.toastr.warning("please enter billing address"); return;
    }

    if (bilCity === "") {
        $.toastr.warning("please enter billing city"); return;
    }

    if (bilState === "") {
        $.toastr.warning("please enter billing state"); return;
    }

    if (bilZipCode === "") {
        $.toastr.warning("please enter billing zip code"); return;
    }

    let data = {
        accountType: accountType,
        firstName: firstName,
        lastName: lastName,
        businessName: businessName,
        address: address,
        city: city,
        state: state,
        zipCode: zipCode,
        phoneNumber: phoneNumber,
        email: email,
        website: website,
        marketCode: marketCode,
        salesPerson: salesPerson,
        submitter: submitter,
        legacyId: legacyId,
        bilEmail: bilEmail,
        bilAddress: addressFlag == 0 ? bilAddress : address,
        bilCity: addressFlag == 0 ? bilCity : city,
        bilState: addressFlag == 0 ? bilState : state,
        bilZipCode: addressFlag == 0 ? bilZipCode : zipCode
    }

    fetch('/advertising/register-advertiser/', {
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

        setTimeout(goNewCampaign(data['id']), 500);
    })
    .catch(error => {
        $.toastr.error("Saved failure");
    });
}
function updateAdvertiser() {
    let advertiserId = document.getElementById("current-account-id").value; 

    let accountType = parseInt(document.getElementById("account-type").value);
    let firstName = document.getElementById("contact_name_first-name").value;
    let lastName = document.getElementById("contact_name_last-name").value;
    let businessName = document.getElementById("business-name").value;
    let address = document.getElementById("address").value;
    let city = document.getElementById("city").value;
    let state = document.getElementById("state").value;
    let zipCode = document.getElementById("zip-code").value;
    let phoneNumber = document.getElementById("phone-number").value;
    let email = document.getElementById("email").value;
    let website = document.getElementById("website").value;
    let marketCode = parseInt(document.getElementById("market-code").value);
    let salesPerson = parseInt(document.getElementById("sales-person").value);
    let submitter = document.getElementById("submitter").value;
    let legacyId = document.getElementById("legacy-id").value;
    let bilEmail = document.getElementById("billing-email").value;
    let bilAddress = document.getElementById("billing-address").value;
    let bilCity = document.getElementById("billing-city").value;
    let bilState = document.getElementById("billing-state").value;
    let bilZipCode = document.getElementById("billing-zip-code").value;

    if (accountType === 0) {
        $.toastr.warning("Please select account type"); return;
    }

    if (firstName === "") {
        $.toastr.warning("please enter first name"); return;
    }

    if (lastName === "") {
        $.toastr.warning("please enter last name"); return;
    }

    if (businessName === "") {
        $.toastr.warning("please enter business name"); return;
    }

    if (address === "") {
        $.toastr.warning("please enter address"); return;
    }

    if (city === "") {
        $.toastr.warning("please enter city"); return;
    }

    if (state === "") {
        $.toastr.warning("please select state"); return;
    }

    if (zipCode === "") {
        $.toastr.warning("please enter zip code"); return;
    }

    if (phoneNumber === "") {
        $.toastr.warning("please enter phone number"); return;
    }

    if (email === "") {
        $.toastr.warning("please enter email"); return;
    }

    if (website === "") {
        $.toastr.warning("please enter website"); return;
    }

    if (marketCode === 0) {
        $.toastr.warning("please enter market code"); return;
    }

    if (salesPerson === 0) {
        $.toastr.warning("please enter sales person"); return;
    }

    if (submitter === "") {
        $.toastr.warning("please enter submitter"); return;
    }

    if (legacyId === "") {
        $.toastr.warning("please enter legacy id"); return;
    }

    if (bilEmail === "") {
        $.toastr.warning("please enter billing email"); return;
    }

    if (bilAddress === "") {
        $.toastr.warning("please enter billing address"); return;
    }

    if (bilCity === "") {
        $.toastr.warning("please enter billing city"); return;
    }

    if (bilState === "") {
        $.toastr.warning("please enter billing state"); return;
    }

    if (bilZipCode === "") {
        $.toastr.warning("please enter billing zip code"); return;
    }

    let data = {
        accountType: accountType,
        firstName: firstName,
        lastName: lastName,
        businessName: businessName,
        address: address,
        city: city,
        state: state,
        zipCode: zipCode,
        phoneNumber: phoneNumber,
        email: email,
        website: website,
        marketCode: marketCode,
        salesPerson: salesPerson,
        submitter: submitter,
        legacyId: legacyId,
        bilEmail: bilEmail,
        bilAddress: addressFlag == 0 ? bilAddress : address,
        bilCity: addressFlag == 0 ? bilCity : city,
        bilState: addressFlag == 0 ? bilState : state,
        bilZipCode: addressFlag == 0 ? bilZipCode : zipCode
    }

    fetch('/advertising/edit_new_advertiser/?advertiserId='+`${advertiserId}`, {
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

        setTimeout(goNewCampaign(data['id']), 500);
    })
    .catch(error => {
        $.toastr.error("Saved failure");
    });
}

function goNewCampaign (id) {
    // window.location.href = `/advertising/advertiser_dashboard/?advertiserId=${id}`;
    window.location.href = `/advertising/advertiser_home`
}

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
