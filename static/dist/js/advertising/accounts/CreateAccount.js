const radioToggleBtns = document.querySelectorAll(".radio-toggle input[type='radio']");
const newBillingAddressSection = document.querySelector('#new_billing_address_section');

radioToggleBtns.forEach((input, _, all) => {
    if (input.value == 'different') {
        input.checked = true;
        input.parentElement.classList.add('checked')
    }

    input.onclick = _ => {
        all.forEach(radioBtn => {
            radioBtn.closest('.radio-toggle').classList.toggle('checked', radioBtn.checked);
            newBillingAddressSection.style.display = input.value == 'same' ? 'none' : 'block';
        });
    }
})


const phoneInput = document.querySelector('#phone');

phoneInput.addEventListener("input", () => {
    phoneInput.value = formatPhoneNumber(phoneInput.value);
});

function formatPhoneNumber(phoneNumberString) {
    let cleaned = ('' + phoneNumberString).replace(/\D/g, '');
    let match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);

    if (match) return `(${match[1]}) ${match[2]}-${match[3]}`;
    return phoneNumberString;
}

$(document).ready(function () {
    $("#country").countrySelector();
});