var unitType = $('#unit_type');
var price = $('#unit_price');
var publication = $('#publication');
var locationInput = $('#location');
var sizeInput = $('#size');
var calculateBtn = $('#calculateBtn');
var customSizesBtn = $('#customSizes');

var minHeight = $('input[name="custom_min_height"]');
var minWidth = $('input[name="custom_min_width"]');
var maxHeight = $('input[name="custom_max_height"]');
var maxWidth = $('input[name="custom_max_width"]');

var minHeightVal;
var minWidthVal;
var maxHeightVal;
var maxWidthVal;
var priceVal;

var minPriceTotal = $('#minPrice');
var maxPriceTotal = $('#maxPrice');
var standardRateTotal = $('#standardRateTotal');
var standardRate = $('#standardRate');
var customRateTotal = $('#customRateTotal');

var errorList = $('#errors');
var isCustom = false;

var quarterPage = { name:"Quarter Page", height: 9.84, width: 6.3 };
var halfPage = { name: "Half Page", height: 9.84, width: 12.9 };
var fullPage = { name: "Full Page", height: 20.47, width: 12.9 };

var locations = {
    "prem_insideCover": "Inside Cover (Premium)",
    "prem_backCover": "Back Cover (Premium)",
    "prem_center": "Center (Premium)",
    "static": "Static"
}

var sizes = {
    "quarter": "Quarter Page",
    "half": "Half Page",
    "full": "Full Page"
}

var subtotalSection = $('#subtotal');
var pricePerUnit = $('#pricePerUnit');
var finalUnitType = $('#unitType');
// var finalSize = $('#finalSize');
var finalLocation = $('#finalLocation');
var ratePrice = $('#rate_price');

$(document).ready(() => {
    price.on('input', () => { priceVal = price.val(); });

    standardRateTotal.hide();
    customRateTotal.hide();
    subtotalSection.hide();

    calculateBtn.on('click', (e) => {
        let finalPrice = 0;
        let minPrice = 0;
        let maxPrice = 0;

        $.ajax({
            url: '/advertising/ajax/rate/get-rate-location/',
            type: 'POST',
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },
            data: JSON.stringify({
                'location': locationInput.val(),
                'publication': Number(publication.val()),
            }),
            success: (data) => {
                if (data.rate) {
                    finalPrice += data.rate.price;
                    standardRate.text(finalPrice.toFixed(2));
                    errorList.text('');

                    minPrice += data.rate.price;
                    maxPrice += data.rate.price;

                    minPriceTotal.text(minPrice + finalPrice);
                    maxPriceTotal.text(maxPrice + finalPrice);
                }
                
            }, error: (err) => {
                console.error(err);
            }
        });

        if (pricePerUnit.val() == '') {
            pricePerUnit.val(0);
        } else if (pricePerUnit == null) {
            pricePerUnit.val(0);
        } else if (pricePerUnit.val() == 'NaN') {
            pricePerUnit.val(0);
        }

        if (isNaN(finalPrice)) {
            finalPrice = 0;
        }

        finalUnitType.text(unitType.val());
        pricePerUnit.text(priceVal);
        
        finalLocation.text(locations[locationInput.val()]);
        standardRate.text(finalPrice.toFixed(2));
        ratePrice.val(finalPrice.toFixed(2));

        var formData = $('#new_rate_form').serializeArray();

        subtotalSection.show();
    });
    $('#new_rate_form').submit(function(e) {
        var formData = $(this).serializeArray();
    });
});

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}