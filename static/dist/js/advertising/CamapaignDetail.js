function collapseEditSpec(clickedButton) {
    const childElements = clickedButton.childNodes;

    for (var i = 0; i < childElements.length; i++) {
        var item = childElements[i];
        if (item.nodeName === "svg") {
            if (item.classList.contains("c-svg-active")) {
                item.classList.remove("c-svg-active");
            } else {
                item.classList.add("c-svg-active");
            }
        }
    }
}

function collapseEditSpecItem(clickedButton, demo, publication, ad, type) {
    collapseEditSpec(clickedButton);

    let elementId = type === 0 ? "ad-content-" : "sum-ad-content-";
    debugger;
    const specItem = document.getElementById(elementId + demo + "-" + publication + "-" + ad);
    const display = specItem.style.display;

    if (display === "none") {
        specItem.style.display = "block";
    } else {
        specItem.style.display = "none";
    }

    let adElementId = type === 0 ? "edit-ad-item-" : "sum-edit-ad-item-";

    const adSpecItem = document.getElementById(adElementId + demo + "-" + publication + "-" + ad);
    const maxHeight = adSpecItem.style.maxHeight;

    if (maxHeight === "inherit") {
        adSpecItem.style.maxHeight = "55px";
    } else {
        adSpecItem.style.maxHeight = "inherit";
    }
}

function EditCampaign() {
    var campaignName = document.getElementById("campaign-name").value;

    if (campaignName === "") {
        $.toastr.warning("Please complete the fields");
        return;
    }

    let salesContact_id = document.getElementById("sales-contact").value;

    if (salesContact_id === "") {
        $.toastr.warning("Please complete the fields");
        return;
    }

    var startDate = document.getElementById("start-date").value;

    if (startDate === "") {
        $.toastr.warning("Please complete the fields");
        return;
    }

    const data = {
        campaignName: campaignName,
        salesContact: salesContact_id,
        startDate: startDate,
        endDate: document.getElementById("end-date").value,
        brief: document.getElementById("brief").value,
    }
}

const getCookie = name => {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}

function editAdItem(demo, pub, ad) {
    editAdSel = ad;
    console.log(demo, pub, ad);

    let adName = document.getElementById("sum-ad-name-" + demo + "-" + pub + "-" + ad).innerText;
    let adType = document.getElementById("sum-ad-type-" + demo + "-" + pub + "-" + ad).innerText;
    let adSize = document.getElementById("sum-ad-size-" + demo + "-" + pub + "-" + ad).innerText;
    let adRate = document.getElementById("sum-ad-rate-" + demo + "-" + pub + "-" + ad).innerText;
    let adBrief = document.getElementById("sum-ad-brief-" + demo + "-" + pub + "-" + ad).innerText;

    let adAdjEle = document.getElementById("sum-adjustment-item-" + demo + "-" + pub + "-" + ad);
    let adAdjList = getChildNodeList(adAdjEle);

    let innerHtml = "";
    selectedAdjustmentArray = [];
    for (let m = 0; m < adAdjList.length; m ++) {
        let adjItem = adAdjList[m];

        let code = adjItem.querySelector("#sum-ad-adj-code").innerText;
        let amount = adjItem.querySelector("#sum-ad-adj-amount").innerText;
        let id = adjItem.querySelector("#sum-ad-adj-id").value;

        innerHtml += `<div id="adjustments_list-` + id + `" class="mt-1 flex-row sel-adjustment">
                        <h5 id="ad-adj-code" class="black">` + code + `</h5>
                        <h5 id="ad-adj-amount" class="black">` + amount + `</h5>
                        <input id="ad-adj-id" type="hidden" value="` + id + `">
                      </div>`;

        selectedAdjustmentArray.push(id);


        // document.getElementById("adjustment-select-" + id).style.visibility = "visible";
    }

    let adRateId = "";

    for (let i = 0; i < ratingList.length; i ++) {
        let item = ratingList[i];

        if (item.fields['name'] === adRate) {
            adRateId = item.pk;
        }
    }

    document.getElementById("ad-name").value = adName;
    document.getElementById("ad-type").value = adType;
    document.getElementById("ad-size").value = adSize;
    document.getElementById("ad-rate").value = adRateId;
    document.getElementById("ad-brief").value = adBrief;
    document.getElementById("adjustment-value").innerHTML = innerHtml;

    editAdFlag = true;
}

function getChildNodeList(element) {
    let elementList = element.childNodes;

    for (let index = 0; index < elementList.length; index ++) {
        if (elementList[index].tagName !== "DIV") {
            element.removeChild(elementList[index]);
            index --;
        }
    }

    return element.childNodes;
}