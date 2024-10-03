let selectedAdFormatsName = [];

let demo_index = 0;
let pub_index = 0;

let pub_option_list = document.getElementById("publication_data").innerHTML

let selectedAdjustmentArray = [];

let storedID = "";

let editAdFlag = false;

let editAdSel = "";

let originalAdTypeOptions = '';
let originalAdAdjustmentOptions = '';



function selectAdFormat(public_id) {

    const selected_img = document.getElementById("favoriteIcon_" + public_id);
    const selected_name = document.getElementById("adTypeName_" + public_id).innerText;

    let adFormatHoverEle = document.getElementById("ad-format-hover-" + public_id);

    const visibility = selected_img.style.visibility;

    if (visibility === 'visible') {
        selected_img.style.visibility = 'hidden';
        const index = selectedAdFormatsName.indexOf(selected_name);
        if (index !== -1)
            selectedAdFormatsName.splice(index, 1);
        adFormatHoverEle.innerHTML = "Add to <br> Campaign!";
        adFormatHoverEle.style.opacity = 1;
        
    } else {
        selected_img.style.visibility = 'visible';
        selectedAdFormatsName.push(selected_name);
        // adFormatHoverEle.innerHTML = "Added to <br> Campaign!";
        adFormatHoverEle.style.opacity = 0;
    }
}

function showNextStep(currentStep, nextStepId) {
    // Show the next step if it exists
    console.log(nextStepId)
    let nextStepElement = document.getElementById(nextStepId);
    if (nextStepElement) {
        nextStepElement.style.display = "block";
        if(nextStepId == 'ad-adjustment-step') {
            nextStepElement.style.display = "flex";
        }
        else nextStepElement.style.display = "block";
    }

    else {
        console.error("Element with ID '" + nextStepId + "' not found.");
    }
}

function selectStar(public_id) {
    var selected_img = document.getElementById("star_" + public_id);

    var source = selected_img.src;

    if (source.includes('Star-white')) {
        selected_img.src = '/static/svg/Star-golden.svg';
    } else {
        selected_img.src = '/static/svg/Star-white.svg';
    }
}

function addAdjustment() {
    let parent = document.getElementById("adjustment-value");
    let innerHtml = "";

    for (let i = 0; i < selectedAdjustmentArray.length; i ++) {
        let code = document.getElementById("adjustment-code-" + selectedAdjustmentArray[i]).innerHTML;
        let amount = document.getElementById("adjustment-amount-" + selectedAdjustmentArray[i]).innerHTML;

        innerHtml += `<div id="adjustments_list-` + selectedAdjustmentArray[i] + `" class="mt-1 flex-row sel-adjustment">
                        <h5 id="ad-adj-code" class="black">` + code + `</h5>
                        <h5 id="ad-adj-amount" class="black">` + amount + `</h5>
                        <input id="ad-adj-id" type="hidden" value="` + selectedAdjustmentArray[i] + `">
                      </div>`;
    }

    parent.innerHTML = innerHtml;
}

function advertiser_next() {
    var advertiser_id = document.getElementById("search-select").value;
    var advertiser = document.getElementById("select2-search-select-container").innerText;
    if (advertiser_id === "") {
        $.toastr.warning("please select advertiser");
        return;
    }
    document.getElementById("sum-advertiser-id").innerHTML = advertiser_id;
    document.getElementById("sum-advertiser-name").innerHTML = advertiser;
    showSection(2);
}

function campaign_next() {
    var orderName = document.getElementById("order-name").value;

    if (orderName === "") {
        $.toastr.warning("Please complete the fields");
        return;
    } else {
        document.getElementById("sum-campaign-name").innerText = orderName;
    }

    let salesContact_id = document.getElementById("sales-contact").value;

    if (salesContact_id === "") {
        $.toastr.warning("Please complete the fields");
        return;
    } else {
        let salesContact_name = '';

        for (let item in salesPersonList) {
            if (salesPersonList[item].pk == salesContact_id) {
                salesContact_name = salesPersonList[item].fields['first_name'] + salesPersonList[item].fields['last_name'];
            }
        }
        document.getElementById("sum-sales-id").innerText = salesContact_id;
        document.getElementById("sum-sales-name").innerText = salesContact_name;
    }

    var startDate = document.getElementById("start-date").value;

    if (startDate === "") {
        $.toastr.warning("Please complete the fields");
        return;
    } else {
        document.getElementById("sum-start-date").innerText = startDate;
    }

    document.getElementById("sum-end-date").innerText = document.getElementById("end-date").value;

    document.getElementById("sum-brief").innerText = document.getElementById("brief").value;

    showSection(3);
}

// function publication_next() {
//     let summaryEle = document.getElementById("sum-ad-details");
//     let sumPrintTotal = document.getElementById("sum-print-total");
//     let sumAdjTotal = document.getElementById("sum-adj-total");
//     let sumCampaignTotal = document.getElementById("sum-campaign-total");

//     let sumDemoItemListEle = "";
//     let sumPrintTotalValue = "0.00";
//     let sumAdjTotalValue = "0.00";
//     for (let demo_idx = 0; demo_idx < selectedAdFormatsName.length; demo_idx ++) {
//         let pubEle = document.getElementById("spec-item-" + demo_idx);
//         let pubItemList = getChildNodeList(pubEle);

//         let sumPubItemListEle = "";
//         for (let pub_idx = 0; pub_idx < pubItemList.length; pub_idx ++) {
//             let tempPubId = pubItemList[pub_idx].id;
//             let tempPubIndex = tempPubId.charAt(tempPubId.length - 1);

//             let adEle = document.getElementById("edit-ad-" + demo_idx + "-" + tempPubIndex);
//             let adItemList = getChildNodeList(adEle);

//             let sumAdItemListEle = "";
//             for (let ad_idx = 0; ad_idx < adItemList.length; ad_idx ++) {
//                 let tempId = adItemList[ad_idx].id;
//                 let tempAdIndex = tempId.charAt(tempId.length - 1);
//                 let adName = document.getElementById("ad-name-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
//                 let adCount = document.getElementById("ad-count-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).value;
//                 let adUnitPrice = document.getElementById("ad-unit-price-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
//                 let adType = document.getElementById("ad-type-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
//                 let adSize = document.getElementById("ad-size-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
//                 let adRate = document.getElementById("ad-rate-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
//                 let adBrief = document.getElementById("ad-brief-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;

//                 let adjEle = document.getElementById("adjustment-item-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex);
//                 let adjEleList = getChildNodeList(adjEle);

//                 let sumAdjItemListEle = "";
//                 for (let adj_idx = 0; adj_idx < adjEleList.length; adj_idx ++) {
//                     let temp = adjEleList[adj_idx];
//                     let adjName = temp.querySelector("#adj-name").innerText;
//                     let adjAmount = temp.querySelector("#adj-amount").innerText;

//                     sumAdjItemListEle += `<div id="sum-ad-adj-item-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `-` + adj_idx + `" class="flex-row sel-adjustment">
//                                             <h5 id="sum-ad-adj-code" class="black">` + adjName + `</h5>
//                                             <h5 id="sum-ad-adj-amount" class="black">` + adjAmount + `</h5>
//                                           </div>`;
//                 }

//                 sumAdItemListEle += `<div id="sum-edit-ad-item-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="edit-ad-item">
//                                             <div class="edit-ad-item-title">
//                                                 <span id="sum-ad-name-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `">` + adName + `</span>
            
//                                                 <h6>Insertions:</h6>
                                                    
//                                                 <h6 id="sum-ad-count-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" style="margin-left: 5px">` + adCount + `</h6>
            
//                                                 <h4 class="black">$<span id="sum-ad-unit-price-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `">` + adUnitPrice + `</span></h4>
//                                             </div>
            
//                                             <div id="sum-ad-content-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" style="display: none">
//                                                 <div class="value-items">
//                                                     <div class="value-itmes-1-3">
//                                                         <div class="ad-type">
//                                                             <div class="ad-type-label">Ad Type:</div>
//                                                             <div id="sum-ad-type-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + adType + `</div>
//                                                         </div>
//                                                     </div>
//                                                     <div class="value-itmes-1-3">
//                                                         <div class="ad-type">
//                                                             <div class="ad-type-label">Size:</div>
                
//                                                             <div id="sum-ad-size-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + adSize + `</div>
//                                                         </div>
//                                                     </div>
//                                                     <div class="value-itmes-1-3">
//                                                         <div class="ad-date">
//                                                             <div class="ad-type-label">Rates:</div>
                
//                                                             <div id="sum-ad-rate-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + adRate + `</div>
//                                                         </div>
//                                                     </div>
//                                                 </div>
                                
//                                                 <div class="value-items">
//                                                     <div class="ad-date" id="ad-calender-"`+demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `">
//                                                         <div class="ad-type-label">Dates:</div>
                                                        
//                                                         <div style="border: 1px solid #666; border-radius: 4px">
//                                                             <div id="ad-calendar-controls">
//                                                                 <select id="ad-sum-year-selector" class="form-select">
//                                                                     <!-- Add options for years (e.g., 2022, 2023, etc.) -->
//                                                                 </select>
                                                                
//                                                                 <select id="ad-sum-month-selector" class="form-select">
//                                                                 <!-- Add options for months (1-12) -->
//                                                                 </select>
                    
//                                                                 <button id="ad-sum-prev-month-btn" class="arrow-btn">&#8595;</button>
                                                                
//                                                                 <button id="ad-sum-next-month-btn" class="arrow-btn">&#8593;</button>
//                                                             </div>
                                                            
//                                                             <div id="ad-sum-calendar"></div>
//                                                         </div>
//                                                     </div>
//                                                 </div>
                
//                                                 <div class="adjustment-label">Adjustments:</div>
                
//                                                 <div id="sum-adjustment-item-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="adjustment-value">
//                                                     ` + sumAdjItemListEle + `
//                                                 </div>
                
//                                                 <div class="c-ad-value-description">
//                                                     <div class="adjustment-label">Description:</div>
                
//                                                     <div id="sum-ad-brief-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + adBrief + `</div>
//                                                 </div>
//                                             </div>
            
//                                             <div class="collapse-icon" onclick="collapseEditSpecItem(this, ` + demo_idx + `, ` + tempPubIndex + `, ` + tempAdIndex + `, 1)">
//                                                 <svg class="c-svg-active" xmlns="http://www.w3.org/2000/svg"
//                                                      width="16" height="9" viewBox="0 0 16 9" fill="none">
//                                                     <path d="M7.29289 8.70711C7.68342 9.09763 8.31658 9.09763 8.70711 8.70711L15.0711 2.34315C15.4616 1.95262 15.4616 1.31946 15.0711 0.928932C14.6805 0.538408 14.0474 0.538408 13.6569 0.928932L8 6.58579L2.34315 0.928932C1.95262 0.538408 1.31946 0.538408 0.928932 0.928932C0.538408 1.31946 0.538408 1.95262 0.928932 2.34315L7.29289 8.70711ZM7 6V8H9V6H7Z"
//                                                           fill="#F26722"/>
//                                                 </svg>
            
//                                                 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="9"
//                                                      viewBox="0 0 16 9" fill="none">
//                                                     <path d="M8.70711 0.292893C8.31658 -0.097631 7.68342 -0.097631 7.29289 0.292893L0.928932 6.65685C0.538408 7.04738 0.538408 7.68054 0.928932 8.07107C1.31946 8.46159 1.95262 8.46159 2.34315 8.07107L8 2.41421L13.6569 8.07107C14.0474 8.46159 14.6805 8.46159 15.0711 8.07107C15.4616 7.68054 15.4616 7.04738 15.0711 6.65685L8.70711 0.292893ZM9 3V1H7V3H9Z"
//                                                           fill="#F26722"/>
//                                                 </svg>
//                                             </div>
//                                         </div>`;
//             }

//             let selectedPubId = document.getElementById("select-pub-" + demo_idx + "-" + tempPubIndex).value;
//             let selectedPubName = "";
//             let selectedPubPrice = document.getElementById("pub-price-" + demo_idx + "-" + tempPubIndex).innerHTML;

//             for (let item in publicationsList) {
//                 if (publicationsList[item].pk == selectedPubId) {
//                     selectedPubName = publicationsList[item].fields['name']
//                 }
//             }

//             sumPubItemListEle += `<div id="sum-ad-spec-item-` + demo_idx + `-` + tempPubIndex + `" class="c-ad-spec-item">
//                                         <div class="select-publication">
//                                             <span id="sum-select-pub-` + demo_idx + `-` + tempPubIndex + `">` + selectedPubName + `</span>
            
//                                             <h4 class="black">$<span id="sum-pub-price-` + demo_idx + `-` + tempPubIndex + `">` + selectedPubPrice + `</span></h4>
//                                         </div>
            
//                                         <hr class="black">
            
//                                         <div id="sum-edit-ad-` + demo_idx + `-` + tempPubIndex + `" class="edit-ad">
//                                             ` + sumAdItemListEle + `
//                                         </div>
//                                     </div>`;
//         }

//         let printAdPrice = document.getElementById("print-ad-price-" + demo_idx).innerHTML;
//         let printAdjPrice = document.getElementById("print-adj-price-" + demo_idx).innerHTML;
//         let printTotalPrice = document.getElementById("print-total-price-" + demo_idx).innerHTML;

//         sumPrintTotalValue = parseFloat(sumPrintTotalValue) + parseFloat(printAdPrice);
//         sumAdjTotalValue = parseFloat(sumAdjTotalValue) + parseFloat(printAdjPrice);

//         sumDemoItemListEle += `<div class="c-m-panel">
//                                     <div class="btn secondary c-section" data-toggle="collapse" data-target="#sum-demo-` + demo_idx + `"
//                                          onclick="collapseEditSpec(this)">
//                                         ` + selectedAdFormatsName[demo_idx] + `
//                                         <svg class="c-svg-active" xmlns="http://www.w3.org/2000/svg" width="24" height="14"
//                                              viewBox="0 0 24 14" fill="none">
//                                             <path d="M10.9393 13.0607C11.5251 13.6464 12.4749 13.6464 13.0607 13.0607L22.6066 3.51472C23.1924 2.92893 23.1924 1.97919 22.6066 1.3934C22.0208 0.807611 21.0711 0.807611 20.4853 1.3934L12 9.87868L3.51472 1.3934C2.92893 0.807611 1.97919 0.807611 1.3934 1.3934C0.807611 1.97919 0.807611 2.92893 1.3934 3.51472L10.9393 13.0607ZM10.5 11V12H13.5V11H10.5Z"
//                                                   fill="#666666"/>
//                                         </svg>
        
//                                         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="14" viewBox="0 0 24 14"
//                                              fill="none">
//                                             <path d="M13.0607 0.93934C12.4749 0.353553 11.5251 0.353553 10.9393 0.93934L1.3934 10.4853C0.807611 11.0711 0.807611 12.0208 1.3934 12.6066C1.97919 13.1924 2.92893 13.1924 3.51472 12.6066L12 4.12132L20.4853 12.6066C21.0711 13.1924 22.0208 13.1924 22.6066 12.6066C23.1924 12.0208 23.1924 11.0711 22.6066 10.4853L13.0607 0.93934ZM13.5 3V2L10.5 2V3L13.5 3Z"
//                                                   fill="#666666"/>
//                                         </svg>
//                                     </div>
        
//                                     <div id="sum-demo-` + demo_idx + `" class="collapse secondary p-2 c-ad-spec">
//                                         <div id="sum-spec-item-` + demo_idx + `">
//                                            ` + sumPubItemListEle + `
//                                         </div>
        
//                                         <hr class="black mt-1" style="color: #666">
        
//                                         <div class="price-label" style="margin-top: 6px">
//                                             <h5>` + selectedAdFormatsName[demo_idx] + ` Ad(s) Subtotal:</h5>
        
//                                             <h5 class="c-mr-50">$<span id="sum-print-ad-price-` + demo_idx + `" >` + printAdPrice + `</span></h5>
//                                         </div>
        
//                                         <div class="price-label">
//                                             <h5>Adjustment Total:</h5>
        
//                                             <h5 class="c-mr-50">$<span id="sum-print-adj-price-` + demo_idx + `">` + printAdjPrice + `</span></h5>
//                                         </div>
        
//                                         <div class="price-label">
//                                             <h4>` + selectedAdFormatsName[demo_idx] + ` Ad(s) Total:</h4>
        
//                                             <h4 class="c-mr-50">$<span id="sum-print-total-price-` + demo_idx + `">` + printTotalPrice + `</span></h4>
//                                         </div>
//                                     </div>
//                                 </div>`;
//     }

//     summaryEle.innerHTML = sumDemoItemListEle;
//     sumPrintTotal.innerHTML = sumPrintTotalValue;
//     sumAdjTotal.innerHTML = sumAdjTotalValue;
//     sumCampaignTotal.innerHTML = (parseFloat(sumPrintTotalValue) + parseFloat(sumAdjTotalValue)).toString();

//     showSection(5);
//     drawadCalendar();
// }

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

function adjustment_select(selectedItem, id) {
    let selectLabel = selectedItem.querySelector(".adjustment-select");
    const visibility = selectLabel.style.visibility;

    if (visibility === 'visible') {
        selectLabel.style.visibility = 'hidden';
        const index = selectedAdjustmentArray.indexOf(id.toString());
        if (index !== -1)
            selectedAdjustmentArray.splice(index, 1);
    } else {
        selectLabel.style.visibility = 'visible';
        selectedAdjustmentArray.push(id);
    }
}
function getSelectedPublicationId(selectElementId) {

    let selectElement = document.getElementById(selectElementId);
    return selectElement.options[selectElement.selectedIndex].value;  // Assuming the value contains the publication ID
}
function adFormat_next() {
    const spec_item = document.getElementById("spec-area");
    let innerHtml = "";

    for (let index = 0; index < selectedAdFormatsName.length; index++) {
        console.log(pub_option_list)
        // Parse the HTML string into a document
        let parser = new DOMParser();
        let doc = parser.parseFromString(pub_option_list, 'text/html');

        // Select all option elements
        let options = doc.querySelectorAll('option');

        // Define the product type you want to filter by
        let desiredProductType = selectedAdFormatsName[index].toLowerCase(); // Change this to your desired product type
        let validProductTypes = ['newspaper', 'magazine', 'digital'];

        let filteredOptions;
        if (validProductTypes.includes(desiredProductType)) {
            // Filter options based on the desired product type if it's valid
            filteredOptions = Array.from(options).filter(option => {
                return option.getAttribute('data-product-type') === desiredProductType;
            });
        } else {
            // Return remaining options if the desired product type is not valid
            filteredOptions = Array.from(options).filter(option => {
                return !validProductTypes.includes(option.getAttribute('data-product-type'));
            });
        }
        // Construct a new HTML string with the filtered options
        let filteredPubOptionList = filteredOptions.map(option => option.outerHTML).join('\n');
        let temp = `<div class="c-m-panel">
                            <div class="btn secondary c-section" data-toggle="collapse" data-target="#demo` + index + `"
                                 onclick="collapseEditSpec(this)">
                                ` + selectedAdFormatsName[index] + `
                                <svg class="c-svg-active" xmlns="http://www.w3.org/2000/svg" width="24" height="14"
                                     viewBox="0 0 24 14" fill="none">
                                    <path d="M10.9393 13.0607C11.5251 13.6464 12.4749 13.6464 13.0607 13.0607L22.6066 3.51472C23.1924 2.92893 23.1924 1.97919 22.6066 1.3934C22.0208 0.807611 21.0711 0.807611 20.4853 1.3934L12 9.87868L3.51472 1.3934C2.92893 0.807611 1.97919 0.807611 1.3934 1.3934C0.807611 1.97919 0.807611 2.92893 1.3934 3.51472L10.9393 13.0607ZM10.5 11V12H13.5V11H10.5Z"
                                          fill="#666666"/>
                                </svg>

                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="14" viewBox="0 0 24 14"
                                     fill="none">
                                    <path d="M13.0607 0.93934C12.4749 0.353553 11.5251 0.353553 10.9393 0.93934L1.3934 10.4853C0.807611 11.0711 0.807611 12.0208 1.3934 12.6066C1.97919 13.1924 2.92893 13.1924 3.51472 12.6066L12 4.12132L20.4853 12.6066C21.0711 13.1924 22.0208 13.1924 22.6066 12.6066C23.1924 12.0208 23.1924 11.0711 22.6066 10.4853L13.0607 0.93934ZM13.5 3V2L10.5 2V3L13.5 3Z"
                                          fill="#666666"/>
                                </svg>
                            </div>

                            <div id="demo` + index + `" class="collapse secondary p-2 c-ad-spec">
                                <div id="spec-item-` + index + `">
                                    <div id="ad-spec-item-` + index + `-0" class="c-ad-spec-item">
                                        <div class="c-ad-spec-label">Select Your Publication:</div>
                                        
                                        <div class="select-publication">
                                            <select class="form-control" id="select-pub-` + index + `-0">
                                                ` + filteredPubOptionList  + `
                                            </select>


                                            <button onclick="showAdItemModal(` + index + `, 0, getSelectedPublicationId('select-pub-` + index + `-0'))" data-target="#create-ad" data-toggle="modal">
                                            + Start An Ad For This Publication
                                            </button>

                                            <h4 class="black">$<span id="pub-price-` + index + `-0">0.00</span></h4>
                                        </div>

                                        <hr class="black">

                                        <div id="edit-ad-` + index + `-0" class="edit-ad">
                                            
                                        </div>
                                    </div>
                                </div>

                                <div class="ad-option-button">
                                    <div id="new-pub-` + index + `" class="ad-option-button-item" onclick="createNewPub(` + index + `,'` + desiredProductType + `')">
                                        + Add a publication
                                    </div>

                                    <div class="ad-option-button-item update-button" onclick="updateTotal(` + index + `)">Update Total</div>
                                </div>

                                <hr class="black mt-1" style="color: #666">

                                <div class="price-label" style="margin-top: 6px">
                                    <h5>` + selectedAdFormatsName[index] + ` Ad(s) Subtotal:</h5>

                                    <h5 class="c-mr-50">$<span id="print-ad-price-` + index + `" >0.00</span></h5>
                                </div>

                                <div class="price-label">
                                    <h5>Adjustment Total:</h5>

                                    <h5 class="c-mr-50">$<span id="print-adj-price-` + index + `">0.00</span></h5>
                                </div>

                                <div class="price-label">
                                    <h4>` + selectedAdFormatsName[index] + ` Ad(s) Total:</h4>

                                    <h4 class="c-mr-50">$<span id="print-total-price-` + index + `">0.00</span></h4>
                                </div>
                            </div>
                        </div>`;

        innerHtml += temp;
    }
    spec_item.innerHTML = innerHtml;

    showSection(4);
}
function getCampaignDetail() {
    let campaignDetailEle = document.getElementById("sum-ad-details");
    let campaignDetailList = getChildNodeList(campaignDetailEle);

    let campaignArray = [];
    for (let demo_idx = 0; demo_idx < campaignDetailList.length; demo_idx ++) {
        let campaignName = selectedAdFormatsName[demo_idx];
        let subAdPrice = document.getElementById("sum-print-ad-price-" + demo_idx).innerText;
        let subAdjPrice = document.getElementById("sum-print-adj-price-" + demo_idx).innerText;
        let subTotalPrice = document.getElementById("sum-print-total-price-" + demo_idx).innerText;
        let pubArray = [];

        let cdPubEle = document.getElementById("sum-spec-item-" + demo_idx);
        let cdPubList = getChildNodeList(cdPubEle);
        for (let pub_idx = 0; pub_idx < cdPubList.length; pub_idx ++) {
            let tempPubId = cdPubList[pub_idx].id;
            let tempPubIndex = tempPubId.charAt(tempPubId.length - 1);

            let pubName = document.getElementById("sum-select-pub-" + demo_idx + "-" + tempPubIndex).innerText;
            let pubPrice = document.getElementById("sum-pub-price-" + demo_idx + "-" + tempPubIndex).innerText;
            let adArray = [];

            let cdAdEle = document.getElementById("sum-edit-ad-" + demo_idx + "-" + tempPubIndex);
            let dAdList = getChildNodeList(cdAdEle);
            for (let ad_idx = 0; ad_idx < dAdList.length; ad_idx ++) {
                let tempId = dAdList[ad_idx].id;
                let tempAdIdx = tempId.charAt(tempId.length - 1);

                let adName = document.getElementById("sum-ad-name-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let adCount = document.getElementById("sum-ad-count-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let adPrice = document.getElementById("sum-ad-unit-price-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let adType = document.getElementById("sum-ad-type-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let adSize = document.getElementById("sum-ad-size-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let adRate = document.getElementById("sum-ad-rate-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;

                // Additional fields
                let columns = document.getElementById("sum-ad-columns-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let length = document.getElementById("sum-ad-length-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let words = document.getElementById("sum-ad-words-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let lines = document.getElementById("sum-ad-lines-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let units = document.getElementById("sum-ad-units-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let section = document.getElementById("sum-ad-section-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let pageNum = document.getElementById("sum-ad-pageNum-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let pubDate = document.getElementById("sum-ad-pubDate-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText.split(', ');

                let accountNotes = document.getElementById("sum-account-notes-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let designNotes = document.getElementById("sum-design-notes-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let designNotesFileUpload = document.getElementById("sum-design-notes-file-upload-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                
                let layoutNotes = document.getElementById("sum-layout-notes-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;

                let overrideTotal = document.getElementById("override-total-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
                let customTotal = document.getElementById("custom-total-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;

                let adjArray = [];
                let cdAdjEle = document.getElementById("sum-adjustment-item-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx);
                let cdAdjList = getChildNodeList(cdAdjEle);
                for (let adj_idx = 0; adj_idx < cdAdjList.length; adj_idx ++) {
                    let adjItem = cdAdjList[adj_idx];
                    let adjName = adjItem.querySelector("#sum-ad-adj-code").innerText;
                    let adjAmount = adjItem.querySelector("#sum-ad-adj-amount").innerText;

                    adjArray.push({
                        adjName: adjName,
                        adjAmount: adjAmount
                    });
                }
                debugger
               
                adArray.push({
                    adName: adName,
                    adCount: adCount,
                    adPrice: adPrice,
                    adType: adType,
                    adSize: adSize,
                    adRate: adRate,
                    columns: columns,
                    length: length,
                    words: words,
                    lines: lines,
                    units: units,
                    section: section,
                    pageNum: pageNum,
                    pubDate: pubDate,
                    accountNotes: accountNotes,
                    designNotes: designNotes,
                    designNotesFileUpload:designNotesFileUpload,
                    layoutNotes: layoutNotes,
                    overrideTotal: overrideTotal,
                    customTotal: customTotal,
                    adjArray: adjArray
                });
            }

            pubArray.push({
                pubName: pubName,
                pubPrice: pubPrice,
                adArray: adArray
            });
        }

        campaignArray.push({
            campaignName: campaignName,
            subAdPrice: subAdPrice,
            subAdjPrice: subAdjPrice,
            subTotalPrice: subTotalPrice,
            pubArray: pubArray
        });
    }

    console.log(campaignArray);
    return campaignArray;
}

function editAdItem(demo, pub, ad) {
    editAdSel = ad;

    let adName = document.getElementById("ad-name-" + demo + "-" + pub + "-" + ad).innerText;
    let adType = document.getElementById("ad-type-" + demo + "-" + pub + "-" + ad).innerText;
    let adSize = document.getElementById("ad-size-" + demo + "-" + pub + "-" + ad).innerText;
    let adRate = document.getElementById("ad-rate-" + demo + "-" + pub + "-" + ad).innerText;

    let columns = document.getElementById("columns-" + demo + "-" + pub + "-" + ad).innerText;
    let length = document.getElementById("length-" + demo + "-" + pub + "-" + ad).innerText;
    let words = document.getElementById("words-" + demo + "-" + pub + "-" + ad).innerText;
    let lines = document.getElementById("lines-" + demo + "-" + pub + "-" + ad).innerText;
    let units = document.getElementById("units-" + demo + "-" + pub + "-" + ad).innerText;
    let section = document.getElementById("section-" + demo + "-" + pub + "-" + ad).innerText;
    let pageNum = document.getElementById("pageNum-" + demo + "-" + pub + "-" + ad).innerText;

    // Retrieve the publication dates array
    let pubDate = document.getElementById("pubDate-" + demo + "-" + pub + "-" + ad).innerText.split(', ');

    let accountNotes = document.getElementById("accountNotes-" + demo + "-" + pub + "-" + ad).innerText;
    let designNotes = document.getElementById("designNotes-" + demo + "-" + pub + "-" + ad).innerText;
    let designNotesFileUpload = document.getElementById("designNotesFileUpload-" + demo + "-" + pub + "-" + ad).innerText;

    let layoutNotes = document.getElementById("layoutNotes-" + demo + "-" + pub + "-" + ad).innerText;

    let overrideTotalChecked = document.getElementById("override-total-" + demo + "-" + pub + "-" + ad).innerText === "Yes";
    let customTotal = document.getElementById("custom-total-" + demo + "-" + pub + "-" + ad).innerText;

    let adAdjEle = document.getElementById("adjustment-item-" + demo + "-" + pub + "-" + ad);
    let adAdjList = getChildNodeList(adAdjEle);

    let innerHtml = "";
    selectedAdjustmentArray = [];
    for (let m = 0; m < adAdjList.length; m++) {
        let adjItem = adAdjList[m];

        let code = adjItem.querySelector("#adj-name").innerText;
        let amount = adjItem.querySelector("#adj-amount").innerText;
        let id = adjItem.querySelector("#adj-id").value;

        innerHtml += `<div id="adjustments_list-` + id + `" class="mt-1 flex-row sel-adjustment">
                        <h5 id="ad-adj-code" class="black">` + code + `</h5>
                        <h5 id="ad-adj-amount" class="black">` + amount + `</h5>
                        <input id="ad-adj-id" type="hidden" value="` + id + `">
                      </div>`;

        selectedAdjustmentArray.push(id);

        document.getElementById("adjustment-select-" + id).style.visibility = "visible";
    }

    let adRateId = "";

    for (let i = 0; i < ratingList.length; i++) {
        let item = ratingList[i];

        if (item.fields['name'] === adRate) {
            adRateId = item.pk;
        }
    }

    document.getElementById("ad-name").value = adName;
    document.getElementById("ad-type").value = adType;
    document.getElementById("ad-size").value = adSize;
    document.getElementById("ad-rate").value = adRateId;
    document.getElementById("columns").value = columns;
    document.getElementById("length").value = length;
    document.getElementById("words").value = words;
    document.getElementById("lines").value = lines;
    document.getElementById("units").value = units;
    document.getElementById("section").value = section;
    document.getElementById("pageNum").value = pageNum;

    // Reset and populate the selected publication dates list
    const selectedDatesList = document.getElementById("selectedDatesList");
    selectedDatesList.innerHTML = "";
    pubDate.forEach(date => {
        const dateItem = document.createElement('div');
        dateItem.classList.add('list-group-item', 'content-between');
        dateItem.innerHTML = `
            <span>${new Date(date).toLocaleDateString()}</span>
            <span><i class="fa fa-solid fa-trash delete-date"></i></span>`;
        dateItem.querySelector('.delete-date').addEventListener('click', function () {
            dateItem.remove();
        });
        selectedDatesList.appendChild(dateItem);
    });

    document.getElementById("accountNotes").querySelector('textarea').value = accountNotes;
    document.getElementById("designNotes").querySelector('textarea').value = designNotes;
    document.getElementById("designNotesFileUpload").value = ""
    document.getElementById("layoutNotes").querySelector('textarea').value = layoutNotes;

    document.getElementById("override-total").checked = overrideTotalChecked;
    document.getElementById("custom-total").value = customTotal;

    document.getElementById("adjustment-value").innerHTML = innerHtml;

    // Set the flag to indicate we are editing an ad
    editAdFlag = true;

    // Adjust the dropdown options to reflect the correct publication
    const pub_id = document.getElementById("select-pub-" + demo + "-" + pub).value;
    const adTypeSelectElement = document.getElementById("ad-type");
    const adjustmentSelectElement = document.getElementById("adjustment-row").querySelectorAll('.adjustment-item');

    // Filter the ad type dropdown based on the publication ID
    const adTypeOptions = adTypeSelectElement.querySelectorAll('option');
    adTypeOptions.forEach(option => {
        if (option.getAttribute('data-publication-id') !== pub_id) {
            option.style.display = 'none';
        } else {
            option.style.display = 'block';
        }
    });

    // Filter the adjustment dropdown based on the publication ID
    adjustmentSelectElement.forEach(option => {
        if (option.getAttribute('data-publication-id') !== pub_id) {
            option.style.display = 'none';
        } else {
            option.style.display = 'block';
        }
    });

    // Ensure that the first visible option is selected in case the ad type was filtered out
    if (adTypeSelectElement.querySelector('option[style*="block"]')) {
        adTypeSelectElement.value = adTypeSelectElement.querySelector('option[style*="block"]').value;
    }
}

function publication_next() {
    let summaryEle = document.getElementById("sum-ad-details");
    let sumPrintTotal = document.getElementById("sum-print-total");
    let sumAdjTotal = document.getElementById("sum-adj-total");
    let sumCampaignTotal = document.getElementById("sum-campaign-total");

    let sumDemoItemListEle = "";
    let sumPrintTotalValue = 0.00;
    let sumAdjTotalValue = 0.00;
    
    for (let demo_idx = 0; demo_idx < selectedAdFormatsName.length; demo_idx++) {
        let pubEle = document.getElementById("spec-item-" + demo_idx);
        let pubItemList = getChildNodeList(pubEle);

        let sumPubItemListEle = "";
        for (let pub_idx = 0; pub_idx < pubItemList.length; pub_idx++) {
            let tempPubId = pubItemList[pub_idx].id;
            let tempPubIndex = tempPubId.charAt(tempPubId.length - 1);

            let adEle = document.getElementById("edit-ad-" + demo_idx + "-" + tempPubIndex);
            let adItemList = getChildNodeList(adEle);

            let sumAdItemListEle = "";
            for (let ad_idx = 0; ad_idx < adItemList.length; ad_idx++) {
                let tempId = adItemList[ad_idx].id;
                let tempAdIndex = tempId.charAt(tempId.length - 1);
                let adName = document.getElementById("ad-name-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let adCount = document.getElementById("ad-count-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).value;
                let adUnitPrice = parseFloat(document.getElementById("ad-unit-price-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML);
                let adType = document.getElementById("ad-type-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let adSize = document.getElementById("ad-size-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let adRate = document.getElementById("ad-rate-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let columns = document.getElementById("columns-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let length = document.getElementById("length-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let words = document.getElementById("words-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let lines = document.getElementById("lines-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let units = document.getElementById("units-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let section = document.getElementById("section-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let pageNum = document.getElementById("pageNum-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let pubDate = document.getElementById("pubDate-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let accountNotes = document.getElementById("accountNotes-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let designNotes = document.getElementById("designNotes-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;
                let designNotesFileUpload = document.getElementById("designNotesFileUpload-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex);

                let layoutNotes = document.getElementById("layoutNotes-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).innerHTML;

                let adjEle = document.getElementById("adjustment-item-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex);
                let adjEleList = getChildNodeList(adjEle);

                let sumAdjItemListEle = "";
                let adjustmentTotal = 0;
                for (let adj_idx = 0; adj_idx < adjEleList.length; adj_idx++) {
                    let temp = adjEleList[adj_idx];
                    let adjName = temp.querySelector("#adj-name").innerText;
                    let adjAmount = parseFloat(temp.querySelector("#adj-amount").innerText.replace('$', ''));

                    adjustmentTotal += adjAmount;

                    sumAdjItemListEle += `<div id="sum-ad-adj-item-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `-` + adj_idx + `" class="flex-row sel-adjustment">
                                            <h5 id="sum-ad-adj-code" class="black">` + adjName + `</h5>
                                            <h5 id="sum-ad-adj-amount" class="black">$` + adjAmount.toFixed(2) + `</h5>
                                          </div>`;
                }

                let subtotal = adUnitPrice * adCount + adjustmentTotal;

                // Check for override total
                let overrideTotalChecked = document.getElementById("override-total-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).checked;
                let customTotal = overrideTotalChecked ? parseFloat(document.getElementById("custom-total-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIndex).value) : subtotal;

                sumAdItemListEle += `<div id="sum-edit-ad-item-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="edit-ad-item">
                                            <div class="edit-ad-item-title">
                                                <span id="sum-ad-name-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `">` + adName + `</span>
            
                                                <h6>Insertions:</h6>
                                                <h6 id="sum-ad-count-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" style="margin-left: 5px">` + adCount + `</h6>
            
                                                <h4 class="black">$<span id="sum-ad-unit-price-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `">` + adUnitPrice.toFixed(2) + `</span></h4>
                                            </div>
            
                                            <div id="sum-ad-content-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" style="display: none">
                                                <div class="value-items">
                                                    <div class="value-itmes-1-3">
                                                        <div class="ad-type">
                                                            <div class="ad-type-label">Ad Type:</div>
                                                            <div id="sum-ad-type-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + adType + `</div>
                                                        </div>
                                                    </div>
                                                    <div class="value-itmes-1-3">
                                                        <div class="ad-size">
                                                            <div class="ad-type-label">Size:</div>
                                                            <div id="sum-ad-size-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + adSize + `</div>
                                                        </div>
                                                    </div>
                                                    <div class="value-itmes-1-3">
                                                        <div class="ad-rate">
                                                            <div class="ad-type-label">Rates:</div>
                                                            <div id="sum-ad-rate-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + adRate + `</div>
                                                        </div>
                                                    </div>
                                                </div>
                                                
                                                <div class="value-items">
                                                    <div class="ad-columns">
                                                        <div class="ad-type-label">Columns:</div>
                                                        <div id="sum-ad-columns-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + columns + `</div>
                                                    </div>
                                                    <div class="ad-length">
                                                        <div class="ad-type-label">Length:</div>
                                                        <div id="sum-ad-length-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + length + `</div>
                                                    </div>
                                                    <div class="ad-words">
                                                        <div class="ad-type-label">Words:</div>
                                                        <div id="sum-ad-words-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + words + `</div>
                                                    </div>
                                                    <div class="ad-lines">
                                                        <div class="ad-type-label">Lines:</div>
                                                        <div id="sum-ad-lines-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + lines + `</div>
                                                    </div>
                                                    <div class="ad-units">
                                                        <div class="ad-type-label">Units:</div>
                                                        <div id="sum-ad-units-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + units + `</div>
                                                    </div>
                                                    <div class="ad-section">
                                                        <div class="ad-type-label">Section:</div>
                                                        <div id="sum-ad-section-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + section + `</div>
                                                    </div>
                                                    <div class="ad-page-num">
                                                        <div class="ad-type-label">Page #:</div>
                                                        <div id="sum-ad-pageNum-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + pageNum + `</div>
                                                    </div>
                                                    <div class="ad-pub-date">
                                                        <div class="ad-type-label">Publish Date:</div>
                                                        <div id="sum-ad-pubDate-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + pubDate + `</div>
                                                    </div>
                                                </div>

                                                <div class="value-items">
                                                    <div class="account-notes">
                                                        <div class="ad-type-label">Account Notes:</div>
                                                        <div id="sum-account-notes-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + accountNotes + `</div>
                                                    </div>
                                                     <div class="design-notes">
                                                        <div class="ad-type-label">Design Notes:</div>
                                                        <div id="sum-design-notes-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + designNotes + `</div>
                                                    </div>
                                                     <div class="design-notes" style="visibility:hidden">
                                                        <div class="ad-type-label">Design Notes:</div>
                                                        <div id="sum-design-notes-file-upload-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + designNotesFileUpload + `</div>
                                                    </div>
                                                    <div class="layout-notes">
                                                        <div class="ad-type-label">Layout Notes:</div>
                                                        <div id="sum-layout-notes-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="ad-type-value">` + layoutNotes + `</div>
                                                    </div>
                                                </div>
                
                                                <div class="adjustment-label">Adjustments:</div>
                                                <div id="sum-adjustment-item-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `" class="adjustment-value">
                                                    ` + sumAdjItemListEle + `
                                                </div>
                                            </div>
                                            
                                            <div class="price-label">
                                                <h5>Subtotal:</h5>
                                                <h5 class="c-mr-50">$<span id="sum-subtotal-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `">` + subtotal.toFixed(2) + `</span></h5>
                                            </div>
                                            
                                            <div class="price-label">
                                                <h5>Custom Total:</h5>
                                                <h5 class="c-mr-50">$<span id="sum-custom-total-` + demo_idx + `-` + tempPubIndex + `-` + tempAdIndex + `">` + customTotal.toFixed(2) + `</span></h5>
                                            </div>
                                        </div>`;
                                        
                sumPrintTotalValue += customTotal;
                sumAdItemListEle += `</div>`;
            }

            let selectedPubId = document.getElementById("select-pub-" + demo_idx + "-" + tempPubIndex).value;
            let selectedPubName = "";
            let selectedPubPrice = parseFloat(document.getElementById("pub-price-" + demo_idx + "-" + tempPubIndex).innerHTML);

            for (let item in publicationsList) {
                if (publicationsList[item].pk == selectedPubId) {
                    selectedPubName = publicationsList[item].fields['name'];
                }
            }

            sumPubItemListEle += `<div id="sum-ad-spec-item-` + demo_idx + `-` + tempPubIndex + `" class="c-ad-spec-item">
                                    <div class="select-publication">
                                        <span id="sum-select-pub-` + demo_idx + `-` + tempPubIndex + `">` + selectedPubName + `</span>
                                        <h4 class="black">$<span id="sum-pub-price-` + demo_idx + `-` + tempPubIndex + `">` + selectedPubPrice.toFixed(2) + `</span></h4>
                                    </div>
                                    <hr class="black">
                                    <div id="sum-edit-ad-` + demo_idx + `-` + tempPubIndex + `" class="edit-ad">
                                        ` + sumAdItemListEle + `
                                    </div>
                                </div>`;
        }

        let printAdPrice = parseFloat(document.getElementById("print-ad-price-" + demo_idx).innerHTML);
        let printAdjPrice = parseFloat(document.getElementById("print-adj-price-" + demo_idx).innerHTML);
        let printTotalPrice = printAdPrice + printAdjPrice;

        sumPrintTotalValue += printTotalPrice;
        sumAdjTotalValue += printAdjPrice;

        sumDemoItemListEle += `<div class="c-m-panel">
                                    <div class="btn secondary c-section" data-toggle="collapse" data-target="#sum-demo-` + demo_idx + `"
                                         onclick="collapseEditSpec(this)">
                                        ` + selectedAdFormatsName[demo_idx] + `
                                        <svg class="c-svg-active" xmlns="http://www.w3.org/2000/svg" width="24" height="14"
                                             viewBox="0 0 24 14" fill="none">
                                            <path d="M10.9393 13.0607C11.5251 13.6464 12.4749 13.6464 13.0607 13.0607L22.6066 3.51472C23.1924 2.92893 23.1924 1.97919 22.6066 1.3934C22.0208 0.807611 21.0711 0.807611 20.4853 1.3934L12 9.87868L3.51472 1.3934C2.92893 0.807611 1.97919 0.807611 1.3934 1.3934C0.807611 1.97919 0.807611 2.92893 1.3934 3.51472L10.9393 13.0607ZM10.5 11V12H13.5V11H10.5Z"
                                                  fill="#666666"/>
                                        </svg>
        
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="14" viewBox="0 0 24 14"
                                             fill="none">
                                            <path d="M13.0607 0.93934C12.4749 0.353553 11.5251 0.353553 10.9393 0.93934L1.3934 10.4853C0.807611 11.0711 0.807611 12.0208 1.3934 12.6066C1.97919 13.1924 2.92893 13.1924 3.51472 12.6066L12 4.12132L20.4853 12.6066C21.0711 13.1924 22.0208 13.1924 22.6066 12.6066C23.1924 12.0208 23.1924 11.0711 22.6066 10.4853L13.0607 0.93934ZM13.5 3V2L10.5 2V3L13.5 3Z" fill="#666666"/>
                                        </svg>
                                    </div>
        
                                    <div id="sum-demo-` + demo_idx + `" class="collapse secondary p-2 c-ad-spec">
                                        <div id="sum-spec-item-` + demo_idx + `">
                                           ` + sumPubItemListEle + `
                                        </div>
        
                                        <hr class="black mt-1" style="color: #666">
        
                                        <div class="price-label" style="margin-top: 6px">
                                            <h5>` + selectedAdFormatsName[demo_idx] + ` Ad(s) Subtotal:</h5>
                                            <h5 class="c-mr-50">$<span id="sum-print-ad-price-` + demo_idx + `" >` + printAdPrice.toFixed(2) + `</span></h5>
                                        </div>
        
                                        <div class="price-label">
                                            <h5>Adjustment Total:</h5>
                                            <h5 class="c-mr-50">$<span id="sum-print-adj-price-` + demo_idx + `">` + printAdjPrice.toFixed(2) + `</span></h5>
                                        </div>
        
                                        <div class="price-label">
                                            <h4>` + selectedAdFormatsName[demo_idx] + ` Ad(s) Total:</h4>
                                            <h4 class="c-mr-50">$<span id="sum-print-total-price-` + demo_idx + `">` + printTotalPrice.toFixed(2) + `</span></h4>
                                        </div>
                                    </div>
                                </div>`;
    }

    summaryEle.innerHTML = sumDemoItemListEle;
    sumPrintTotal.innerHTML = sumPrintTotalValue.toFixed(2);
    sumAdjTotal.innerHTML = sumAdjTotalValue.toFixed(2);
    sumCampaignTotal.innerHTML = (sumPrintTotalValue + sumAdjTotalValue).toFixed(2);

    showSection(5);
    drawadCalendar();
}


function arrayBufferToBase64(buffer) {
    let binary = '';
    let bytes = new Uint8Array(buffer);
    let len = bytes.byteLength;

    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}
function createAdItem() {
    let editAdItem = document.getElementById("edit-ad-" + demo_index + "-" + pub_index);
    let innerHtml = editAdItem.innerHTML;

    let editAdItemChild = getChildNodeList(editAdItem);

    let nextAdItemId = "";
    if (editAdItemChild.length === 0) {
        nextAdItemId = 0;
    } else {
        let latestChildId = editAdItemChild[editAdItemChild.length - 1].id;
        nextAdItemId = parseInt(latestChildId.charAt(latestChildId.length - 1)) + 1;
    }

    let eleAdName = document.getElementById("ad-name");
    let eleAdType = document.getElementById("ad-type");
    let eleAdSize = document.getElementById("ad-size");
    let eleAdRate = document.getElementById("ad-rate");
    let eleAdUnit = document.getElementById("units");
    let eleAdLine= document.getElementById("lines");
    let eleAdWord = document.getElementById("words");

    let selectedOption = eleAdSize.options[eleAdSize.selectedIndex];
    let rateType= eleAdRate.options[eleAdRate.selectedIndex];

    // Retrieve the values
    let adSize = selectedOption.value;
    let adSizeColumn = selectedOption.getAttribute("data-column-size-id");
    let adRateType = rateType.getAttribute("data-column-rate-id");
    let noOfStartingX = rateType.getAttribute("data-column-no-of-x-id");
    let noOfExtraX = rateType.getAttribute("data-column-no-of-extra-x-id");
    let additionalCost = rateType.getAttribute("data-column-additional-cost-");


    let adName = eleAdName.value;
    let adType = eleAdType.value;
    let adRate_id = eleAdRate.value;
    let adUnit = eleAdUnit.value;
    let adLines = eleAdLine.value;
    let adWords = eleAdWord.value;
    const selectedDates = [];

    // Get all selected dates from the list
    const dateItems = document.querySelectorAll('#selectedDatesList .list-group-item:not(.active) span:first-child');
    dateItems.forEach(item => {
        const formattedDate = new Date(item.textContent).toISOString().split('T')[0];
        selectedDates.push(formattedDate);
    });

    let adUnitPrice = '';
    let adRate = "";
    for (let i = 0; i < ratingList.length; i++) {
        let item = ratingList[i];

        if (item.pk == adRate_id) {
            debugger
            if (adRateType == 'Words')
            {
                adUnitPrice = parseFloat(item.fields['base_cost']) + (( parseFloat(eleAdWord.value)-parseFloat(noOfStartingX))/parseFloat(noOfExtraX));
                if (parseFloat(additionalCost) > 0)
                {
                    adUnitPrice = adUnitPrice * parseFloat(additionalCost)
                }

            }
            else if (adRateType =='Lines')
            {
                adUnitPrice = parseFloat(item.fields['base_cost']) + (( parseFloat(eleAdLine.value)-parseFloat(noOfStartingX))/parseFloat(noOfExtraX));
                if (parseFloat(additionalCost) > 0)
                {
                    adUnitPrice = adUnitPrice * parseFloat(additionalCost)
                }
            }
            else if (adRateType =='Units')
            {
                adUnitPrice = parseFloat(item.fields['base_cost']) + (( parseFloat(eleAdUnit.value)-parseFloat(noOfStartingX))/parseFloat(noOfExtraX));
                if (parseFloat(additionalCost) > 0)
                {
                    adUnitPrice = adUnitPrice * parseFloat(additionalCost)
                }
            }
            else if (adRateType =='Digital')
            {
                adUnitPrice = parseFloat(item.fields['base_cost']) + (( parseFloat(eleAdUnit.value)-parseFloat(noOfStartingX))/parseFloat(noOfExtraX));
                if (parseFloat(additionalCost) > 0)
                {
                    adUnitPrice = adUnitPrice * parseFloat(additionalCost)
                }
            }
            else
            {
                adUnitPrice = parseFloat(item.fields['base_cost']) * parseFloat(adSizeColumn);

            }
            adRate = item.fields['name'];
        }
    }

    let columns = document.getElementById("columns").value;
    let length = document.getElementById("length").value;
    let words = document.getElementById("words").value;
    let lines = document.getElementById("lines").value;
    let units = document.getElementById("units").value;
    let section = document.getElementById("section").value;
    let pageNum = document.getElementById("pageNum").value;

    // We now get the publish dates from the selected dates array instead of individual field
    let pubDate = selectedDates.join(', ');

    // Retrieve notes
    let accountNotes = document.getElementById("accountNotes").querySelector('textarea').value;
    let designNotes = document.getElementById("designNotes").querySelector('textarea').value;
    let designNotesFileUpload = document.getElementById("designNotesFileUpload")
    let designNotesFileBase64 = null
    if (designNotesFileUpload && designNotesFileUpload.files.length > 0) {
        let file = designNotesFileUpload.files[0]; // Get the file object
        let fileReader = new FileReader();
        debugger;
        fileReader.readAsArrayBuffer(file); 

        fileReader.onload = function(event) {
            // Store the Base64 string in the global variable
            let arrayBuffer = event.target.result;

            // Convert ArrayBuffer to Base64
            designNotesFileBase64 = arrayBufferToBase64(arrayBuffer);
            console.log('Base64 file:', designNotesFileBase64);
        };

        fileReader.onerror = function(error) {
            console.error("Error reading the file: ", error);
        };
    }
    let layoutNotes = document.getElementById("layoutNotes").querySelector('textarea').value;

    let elePubPrice = document.getElementById("pub-price-" + demo_index + "-" + pub_index);
    let pubPrice = parseFloat(elePubPrice.innerHTML) + parseFloat(adUnitPrice);

    let adjustmentListText = "";
    let adjustmentPrice = 0;
    for (let j = 0; j < selectedAdjustmentArray.length; j++) {
        let adjustmentItem = document.getElementById("adjustments_list-" + selectedAdjustmentArray[j]);
        let adjCode = adjustmentItem.querySelector("#ad-adj-code").innerText;
        let adjAmount = adjustmentItem.querySelector("#ad-adj-amount").innerText;
        let adjId = adjustmentItem.querySelector("#ad-adj-id").value;

        adjustmentPrice += parseInt(adjAmount.slice(1));

        let ad_index = editAdFlag ? editAdSel : nextAdItemId;
        adjustmentListText += `<div id="ad-adj-item-` + demo_index + `-` + pub_index + `-` + ad_index + `-` + j + `">
                                <div id="adj-name">` + adjCode + `</div>
                                <div id="adj-amount">` + adjAmount + `</div>
                                <input id="adj-id" type="hidden" value="` + adjId + `">
                               </div>`;
    }

    // Calculate subtotal including adjustments
    let subtotalPrice = pubPrice + adjustmentPrice;

    // Handle override total and custom total
    let overrideTotalChecked = document.getElementById("override-total").checked;
    let customTotal = document.getElementById("custom-total").value;

    let finalPrice = overrideTotalChecked && customTotal ? parseFloat(customTotal) : subtotalPrice;
    if (selectedDates.length > 0)
    {
        finalPrice = finalPrice * selectedDates.length

    }
    elePubPrice.innerHTML = finalPrice.toFixed(2);

    if (editAdFlag) {
        document.getElementById("ad-name-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adName;
        document.getElementById("ad-unit-price-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adUnitPrice.toFixed(2);
        document.getElementById("ad-type-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adType;
        document.getElementById("ad-size-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adSize;
        document.getElementById("ad-rate-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adRate;
        document.getElementById("adjustment-item-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adjustmentListText;
        document.getElementById("columns-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = columns;
        document.getElementById("length-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = length;
        document.getElementById("words-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = words;
        document.getElementById("lines-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = lines;
        document.getElementById("units-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = units;
        document.getElementById("section-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = section;
        document.getElementById("pageNum-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = pageNum;
        document.getElementById("pubDate-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = pubDate;
        document.getElementById("accountNotes-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = accountNotes;
        document.getElementById("designNotes-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = designNotes;
        document.getElementById("designNotesFileUpload-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = designNotesFileBase64;

        document.getElementById("layoutNotes-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = layoutNotes;
        document.getElementById("override-total-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = overrideTotalChecked;
        document.getElementById("custom-total-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = customTotal;

        getUpdatedPublicationTotalPrice(demo_index, pub_index);
    } else {
        innerHtml += `<div id="edit-ad-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="edit-ad-item">
                            <div class="edit-ad-item-title">
                                <span id="ad-name-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `">` + adName + `</span>
    
                                <h6>Insertions:</h6>
    
                                <input type="text" id="ad-count-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" value="1" 
                                    onkeydown="updatePublicationPrice(event, ` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `)">
    
                                <h4 class="black">$<span id="ad-unit-price-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `">` + adUnitPrice.toFixed(2) + `</span></h4>
                            </div>
                            
                            <div id="ad-content-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" style="display: none">
                                <div class="value-items">
                                    <div class="value-itmes-1-3">
                                        <div class="ad-type">
                                            <div class="ad-type-label">Ad Type:</div>
                                            <div id="ad-type-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + adType + `</div>
                                        </div>
                                    </div>
                                    <div class="value-itmes-1-3">
                                        <div class="ad-size">
                                            <div class="ad-type-label">Size:</div>
                                            <div id="ad-size-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + adSize + `</div>
                                        </div>
                                    </div>
                                    <div class="value-itmes-1-3">
                                        <div class="ad-rate">
                                            <div class="ad-type-label">Rates:</div>
                                            <div id="ad-rate-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + adRate + `</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="value-items">
                                    <div class="ad-date">
                                        <div class="ad-type-label">Publish Date:</div>
                                        <div id="pubDate-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + pubDate + `</div>
                                    </div>
                                    <div class="ad-sections">
                                        <div class="ad-type-label">Section:</div>
                                        <div id="section-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + section + `</div>
                                    </div>
                                    <div class="ad-pageNum">
                                        <div class="ad-type-label">Page #:</div>
                                        <div id="pageNum-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + pageNum + `</div>
                                    </div>
                                </div>

                                <div class="value-items">
                                    <div class="ad-size">
                                        <div class="ad-type-label">Columns:</div>
                                        <div id="columns-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + columns + `</div>
                                    </div>
                                    <div class="ad-size">
                                        <div class="ad-type-label">Length:</div>
                                        <div id="length-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + length + `</div>
                                    </div>
                                    <div class="ad-size">
                                        <div class="ad-type-label">Words:</div>
                                        <div id="words-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + words + `</div>
                                    </div>
                                    <div class="ad-size">
                                        <div class="ad-type-label">Lines:</div>
                                        <div id="lines-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + lines + `</div>
                                    </div>
                                    <div class="ad-size">
                                        <div class="ad-type-label">Units:</div>
                                        <div id="units-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + units + `</div>
                                    </div>
                                </div>

                                <div class="adjustment-label">Adjustments:</div>
                                <div id="adjustment-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="adjustment-value">
                                    ` + adjustmentListText + `
                                </div>

                                <div class="c-ad-value-description">
                                    <div class="adjustment-label">Account Notes:</div>
                                    <div id="accountNotes-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + accountNotes + `</div>
                                </div>

                                <div class="c-ad-value-description">
                                    <div class="adjustment-label">Design Notes:</div>
                                    <div id="designNotes-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + designNotes + `</div>
                                </div>
                        
                                <div class="c-ad-value-description" style="visibility: hidden;">
                                    <div class="adjustment-label">Design Notes File:</div>
                                    <div id="designNotesFileUpload-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + designNotesFileBase64 + `</div>
                                </div>
                                <div class="c-ad-value-description">
                                    <div class="adjustment-label">Layout Notes:</div>
                                    <div id="layoutNotes-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + layoutNotes + `</div>
                                </div>
                                <div class="price-label">
                                    <div class="adjustment-label">Override Total:</div>
                                    <div id="override-total-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + (overrideTotalChecked ? "Yes" : "No") + `</div>
                                </div>

                                <div class="price-label">
                                    <div class="adjustment-label">Custom Total:</div>
                                    <div id="custom-total-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + customTotal + `</div>
                                </div>
                            </div>

                            <div class="collapse-icon" onclick="collapseEditSpecItem(this, ` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `, 0)">
                                <svg class="c-svg-active" xmlns="http://www.w3.org/2000/svg" width="16" height="9" viewBox="0 0 16 9" fill="none">
                                    <path d="M7.29289 8.70711C7.68342 9.09763 8.31658 9.09763 8.70711 8.70711L15.0711 2.34315C15.4616 1.95262 15.4616 1.31946 15.0711 0.928932C14.6805 0.538408 14.0474 0.538408 13.6569 0.928932L8 6.58579L2.34315 0.928932C1.95262 0.538408 1.31946 0.538408 0.928932 0.928932C0.538408 1.31946 0.538408 1.95262 0.928932 2.34315L7.29289 8.70711ZM7 6V8H9V6H7Z" fill="#F26722"/>
                                </svg>

                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="9" viewBox="0 0 16 9" fill="none">
                                    <path d="M8.70711 0.292893C8.31658 -0.097631 7.68342 -0.097631 7.29289 0.292893L0.928932 6.65685C0.538408 7.04738 0.538408 7.68054 0.928932 8.07107C1.31946 8.46159 1.95262 8.46159 2.34315 8.07107L8 2.41421L13.6569 8.07107C14.0474 8.46159 14.6805 8.46159 15.0711 8.07107C15.4616 7.68054 15.4616 7.04738 15.0711 6.65685L8.70711 0.292893ZM9 3V1H7V3H9Z" fill="#F26722"/>
                                </svg>
                            </div>
                            
                            <div id="ad-edit-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId +`"
                                class="ad-edit-item"
                                onclick="editAdItem(` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `)"
                                data-target="#create-ad" data-toggle="modal">
                                <img src="/static/svg/pencil.svg" alt="pencil">
                            </div>
                            
                            <div id="ad-delete-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId +`"
                                class="ad-delete-item"
                                onclick="deleteAdItem(` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `)">
                                <img src="/static/svg/trash.svg" alt="trash">
                            </div>
                        </div>`;

        editAdItem.innerHTML = innerHtml;
    }

    // Reset form fields
    eleAdName.value = "";
    eleAdType.value = "";
    eleAdSize.value = "";
    eleAdRate.value = "";
    document.getElementById("columns").value = "";
    document.getElementById("length").value = "";
    document.getElementById("words").value = "";
    document.getElementById("lines").value = "";
    document.getElementById("units").value = "";
    document.getElementById("section").value = "";
    document.getElementById("pageNum").value = "";
    document.getElementById("pubDate").value = "";
    document.getElementById("accountNotes").querySelector('textarea').value = "";
    document.getElementById("designNotes").querySelector('textarea').value = "";
    document.getElementById("designNotesFileUpload").value = "";
    document.getElementById("layoutNotes").querySelector('textarea').value = "";
    document.getElementById("custom-total").value = "";
    document.getElementById("override-total").checked = false;

    // Clear selected dates and reset the dates selection
    document.getElementById("selectedDatesList").innerHTML = "";
    selectedDates.length = 0;

    // Clear adjustments
    document.getElementById("adjustment-value").innerHTML = "";
    selectedAdjustmentArray = [];
    let selectedAdjustmentList = Array.from(document.querySelectorAll(".adjustment-select"));
    selectedAdjustmentList.forEach(row => {
        row.style.visibility = "hidden";
    });

    resetDropdownOnClose();
}
       

       


function showAdItemModal(demo, pub, pub_id) {
    demo_index = demo;
    pub_index = pub;
    editAdFlag = false;

    // Reset form fields
    document.getElementById("ad-name").value = "";
    document.getElementById("ad-type").value = "";
    document.getElementById("ad-size").value = "";
    document.getElementById("ad-rate").value = "";
    document.getElementById("columns").value = "";
    document.getElementById("length").value = "";
    document.getElementById("words").value = "";
    document.getElementById("lines").value = "";
    document.getElementById("units").value = "";
    document.getElementById("section").value = "";
    document.getElementById("pageNum").value = "";
    document.getElementById("pubDate").value = "";
    document.getElementById("accountNotes").querySelector('textarea').value = "";
    document.getElementById("designNotes").querySelector('textarea').value = "";
    document.getElementById("designNotesFileUpload").value=""
    document.getElementById("layoutNotes").querySelector('textarea').value = "";
    document.getElementById("adjustment-value").innerHTML = "";

    // Reset override total and custom total fields
    document.getElementById("override-total").checked = false;
    document.getElementById("custom-total").value = "";

    const selectedDates = [];

    // Get all selected dates from the list
    const dateItems = document.querySelectorAll('#selectedDatesList .list-group-item:not(.active) span:first-child');
    dateItems.forEach(item => {
        const formattedDate = new Date(item.textContent).toISOString().split('T')[0];
        selectedDates.push(formattedDate);
    });

    selectedAdjustmentArray = [];
    let selectedAdjustmentList = Array.from(document.querySelectorAll(".adjustment-select"));
    selectedAdjustmentList.forEach(row => {
        row.style.visibility = "hidden";
    });

    // Save the original unfiltered options when the modal is first opened
    if (!originalAdTypeOptions) {
        const selectElement = document.getElementById("ad-type");
        originalAdTypeOptions = selectElement.innerHTML;
    }
    if (!originalAdAdjustmentOptions) {
        const selectElement = document.getElementById("adjustment-row");
        originalAdAdjustmentOptions = selectElement.innerHTML;
    }
    const selectElement = document.getElementById("ad-type");
    const options = selectElement.querySelectorAll('option');
    const optionsAdjustment = document.getElementById("adjustment-row").querySelectorAll('.adjustment-item');
    
    options.forEach(option => {
        if (option.getAttribute('data-publication-id') !== pub_id) {
            option.style.display = 'none';
        } else {
            option.style.display = 'block';
        }
    });

    optionsAdjustment.forEach(option => {
        if (option.getAttribute('data-publication-id') !== pub_id) {
            option.style.display = 'none';
        } else {
            option.style.display = 'block';
        }
    });
    
    // Reset the visibility of any previously selected adjustments
    selectedAdjustmentList.forEach(row => {
        row.style.visibility = "hidden";
    });
    
    // Optionally, you could also pre-select the first visible option after filtering
    if (selectElement.querySelector('option[style*="block"]')) {
        selectElement.value = selectElement.querySelector('option[style*="block"]').value;
    }

}



// function createAdItem() {

//     let editAdItem = document.getElementById("edit-ad-" + demo_index + "-" + pub_index);
//     let innerHtml = editAdItem.innerHTML;

//     let editAdItemChild = getChildNodeList(editAdItem);

//     let nextAdItemId = "";
//     if (editAdItemChild.length === 0) {
//         nextAdItemId = 0;
//     } else {
//         let latestChildId = editAdItemChild[editAdItemChild.length - 1].id;
//         nextAdItemId = parseInt(latestChildId.charAt(latestChildId.length - 1)) + 1;
//     }

//     let eleAdName = document.getElementById("ad-name");
//     let eleAdType = document.getElementById("ad-type");
//     let eleAdSize = document.getElementById("ad-size");
//     let eleAdRate = document.getElementById("ad-rate");
//     let selectedOption = eleAdSize.options[eleAdSize.selectedIndex];

//     // Retrieve the values
//     let adSize = selectedOption.value;  // This will get the value of the selected option
//     let adSizeColumn = selectedOption.getAttribute("data-column-size-id");  // 
//     let adName = eleAdName.value;
//     let adType = eleAdType.value;
//     let adRate_id = eleAdRate.value;
//     const selectedDates = [];
        
//     // Get all selected dates from the list
//     const dateItems = document.querySelectorAll('#selectedDatesList .list-group-item:not(.active) span:first-child');
//     dateItems.forEach(item => {
//         const formattedDate = new Date(item.textContent).toISOString().split('T')[0];
//         selectedDates.push(formattedDate);
//     });
//     let adUnitPrice = '';
//     let adRate = "";
//     for (let i = 0; i < ratingList.length; i ++) {
//         let item = ratingList[i];

//         if (item.pk == adRate_id) {
//             adUnitPrice = parseFloat(item.fields['base_cost']) * parseFloat(adSizeColumn);
//             adRate = item.fields['name'];
//         }
//     }

//     let elePubPrice = document.getElementById("pub-price-" + demo_index + "-" + pub_index);
//     let pubPrice = elePubPrice.innerHTML;
//     pubPrice = parseFloat(pubPrice) + parseFloat(adUnitPrice) ;

//     let adjustmentListText = "";
//     let adjustmentPrice = 0;
//     for (let j = 0; j < selectedAdjustmentArray.length; j ++) {
//         let adjustmentItem = document.getElementById("adjustments_list-" + selectedAdjustmentArray[j]);
//         let adjCode = adjustmentItem.querySelector("#ad-adj-code").innerText;
//         let adjAmount = adjustmentItem.querySelector("#ad-adj-amount").innerText;
//         let adjId = adjustmentItem.querySelector("#ad-adj-id").value;

//         adjustmentPrice += parseInt(adjAmount.slice(1));

//         let ad_index = "";
//         ad_index = editAdFlag ? ad_index = editAdSel : nextAdItemId;
//         adjustmentListText += `<div id="ad-adj-item-` + demo_index + `-` + pub_index + `-` + ad_index + `-` + j + `">
//                                 <div id="adj-name">` + adjCode + `</div>
                                
//                                 <div id="adj-amount">` + adjAmount + `</div>
                                
//                                 <input id="adj-id" type="hidden" value="` + adjId + `">
//                                </div>`;
//     }

//     elePubPrice.innerHTML = pubPrice + adjustmentPrice;

//     if (editAdFlag) {
//         document.getElementById("ad-name-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adName;
//         document.getElementById("ad-unit-price-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adUnitPrice;
//         document.getElementById("ad-type-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adType;
//         document.getElementById("ad-size-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adSize;
//         document.getElementById("ad-rate-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adRate;
//         document.getElementById("adjustment-item-" + demo_index + "-" + pub_index + "-" + editAdSel).innerHTML = adjustmentListText;

//         getUpdatedPublicationTotalPrice(demo_index, pub_index);
//     } else {
//         innerHtml += `<div id="edit-ad-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="edit-ad-item">
//                             <div class="edit-ad-item-title">
//                                 <span id="ad-name-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `">` + adName + `</span>
    
//                                 <h6>Insertions:</h6>
    
//                                 <input type="text" id="ad-count-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" value="1" 
//                                     onkeydown="updatePublicationPrice(event, ` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `)">
    
//                                 <h4 class="black">$<span id="ad-unit-price-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `">` + adUnitPrice + `</span></h4>
//                             </div>
                            
//                             <div id="ad-content-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" style="display: none">
//                                 <div class="value-items">
//                                     <div class="value-itmes-1-3">
//                                         <div class="ad-type">
//                                             <div class="ad-type-label">Ad Type:</div>
//                                             <div id="ad-type-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + adType + `</div>
//                                         </div>
//                                     </div>
//                                     <div class="value-itmes-1-3">
//                                         <div class="ad-type">
//                                             <div class="ad-type-label">Size:</div>

//                                             <div id="ad-size-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + adSize + `</div>
//                                         </div>
//                                     </div>
//                                     <div class="value-itmes-1-3">
//                                         <div class="ad-date">
//                                             <div class="ad-type-label">Rates:</div>

//                                             <div id="ad-rate-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">` + adRate + `</div>
//                                         </div>
//                                     </div>
//                                 </div>
                                
//                                 <div class="value-items">
//                                     <div class="ad-date">
//                                         <div class="ad-type-label">Dates:</div>
                                        
//                                         <div style="border: 1px solid #666; border-radius: 4px">
//                                             <div id="ad-calendar-controls">
//                                                 <select id="ad-year-selector" class="form-select">
//                                                     <!-- Add options for years (e.g., 2022, 2023, etc.) -->
//                                                 </select>
//                                                 <select id="ad-month-selector" class="form-select">
//                                                 <!-- Add options for months (1-12) -->
//                                                 </select>
    
//                                                 <button id="ad-prev-month-btn" class="arrow-btn">&#8595;</button>
//                                                 <button id="ad-next-month-btn" class="arrow-btn">&#8593;</button>
                                                
//                                             </div>
                                            
//                                             <div id="ad-calendar"></div>
//                                         </div>
//                                     </div>
//                                 </div>

//                                 <div class="adjustment-label">Adjustments:</div>
        
//                                 <div id="adjustment-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="adjustment-value">
//                                     ` + adjustmentListText + `
//                                 </div>
        
//                                 <div class="c-ad-value-description">
//                                     <div class="adjustment-label">Description:</div>
        
//                                     <div id="ad-brief-` + demo_index + `-` + pub_index + `-` + nextAdItemId + `" class="ad-type-value">
//                                         ` + adbrief + `
//                                     </div>
//                                 </div>
//                             </div>
    
//                             <div class="collapse-icon" onclick="collapseEditSpecItem(this, ` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `, 0)">
//                                 <svg class="c-svg-active" xmlns="http://www.w3.org/2000/svg" width="16" height="9" viewBox="0 0 16 9" fill="none">
//                                     <path d="M7.29289 8.70711C7.68342 9.09763 8.31658 9.09763 8.70711 8.70711L15.0711 2.34315C15.4616 1.95262 15.4616 1.31946 15.0711 0.928932C14.6805 0.538408 14.0474 0.538408 13.6569 0.928932L8 6.58579L2.34315 0.928932C1.95262 0.538408 1.31946 0.538408 0.928932 0.928932C0.538408 1.31946 0.538408 1.95262 0.928932 2.34315L7.29289 8.70711ZM7 6V8H9V6H7Z"
//                                           fill="#F26722"/>
//                                 </svg>
    
//                                 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="9" viewBox="0 0 16 9" fill="none">
//                                     <path d="M8.70711 0.292893C8.31658 -0.097631 7.68342 -0.097631 7.29289 0.292893L0.928932 6.65685C0.538408 7.04738 0.538408 7.68054 0.928932 8.07107C1.31946 8.46159 1.95262 8.46159 2.34315 8.07107L8 2.41421L13.6569 8.07107C14.0474 8.46159 14.6805 8.46159 15.0711 8.07107C15.4616 7.68054 15.4616 7.04738 15.0711 6.65685L8.70711 0.292893ZM9 3V1H7V3H9Z"
//                                           fill="#F26722"/>
//                                 </svg>
//                             </div>
                            
//                             <div id="ad-edit-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId +`"
//                                 class="ad-edit-item"
//                                 onclick="editAdItem(` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `)"
//                                 data-target="#create-ad" data-toggle="modal"
//                             >
//                                 <img src="/static/svg/pencil.svg" alt="pencil">
//                             </div>
                            
//                             <div id="ad-delete-item-` + demo_index + `-` + pub_index + `-` + nextAdItemId +`"
//                                 class="ad-delete-item"
//                                 onclick="deleteAdItem(` + demo_index + `, ` + pub_index + `, ` + nextAdItemId + `)"    
//                             >
//                                 <img src="/static/svg/trash.svg" alt="trash">
//                             </div>
//                         </div>`;

//         editAdItem.innerHTML = innerHtml;
//     }

//     eleAdName.value = "";
//     eleAdType.value = "";
//     eleAdSize.value = "";
//     eleAdRate.value = "";

//     document.getElementById("adjustment-value").innerHTML = "";
//     selectedAdjustmentArray = [];
//     let selectedAdjustmentList = Array.from(document.querySelectorAll(".adjustment-select"))

//     selectedAdjustmentList.forEach(row => {
//         row.style.visibility = "hidden";
//     });
//     drawCalendar();
//     resetDropdownOnClose()
// }

function getUpdatedPublicationTotalPrice(demo, pub) {
    let AdEle = document.getElementById("edit-ad-" + demo + "-" + pub);
    let AdList = getChildNodeList(AdEle);

    let pubTotalPrice = 0;
    for (let i = 0; i < AdList.length; i ++) {
        let tempAdItemId = AdList[i].id;
        let AdIdx = tempAdItemId.charAt(tempAdItemId.length - 1);

        let count = parseInt(document.getElementById("ad-count-" + demo + "-" + pub + "-" + AdIdx).value);
        let price = parseInt(document.getElementById("ad-unit-price-" + demo + "-" + pub + "-" + AdIdx).innerText);
        let adPrice = count * price;

        let adjEle = document.getElementById("adjustment-item-" + demo + "-" + pub + "-" + AdIdx);
        let adjList = getChildNodeList(adjEle);

        let adjTotalPrice = 0;
        for (let j = 0; j < adjList.length; j ++) {
            let adjItemEle = adjList[j];
            let adjPrice = parseInt(adjItemEle.querySelector("#adj-amount").innerText.slice(1));

            adjTotalPrice += adjPrice;
        }

        pubTotalPrice = adPrice + adjTotalPrice;
    }

    document.getElementById("pub-price-" + demo + "-" + pub).innerText = pubTotalPrice.toString();
}

function createNewPub(index,desiredProductType) {
    let parser = new DOMParser();
    let doc = parser.parseFromString(pub_option_list, 'text/html');

    // Select all option elements
    let options = doc.querySelectorAll('option');
    let validProductTypes = ['newspaper', 'magazine', 'digital'];

    let filteredOptions;
    if (validProductTypes.includes(desiredProductType)) {
        // Filter options based on the desired product type if it's valid
        filteredOptions = Array.from(options).filter(option => {
            return option.getAttribute('data-product-type') === desiredProductType;
        });
    } else {
        // Return remaining options if the desired product type is not valid
        filteredOptions = Array.from(options).filter(option => {
            return !validProductTypes.includes(option.getAttribute('data-product-type'));
        });
    }
    // Construct a new HTML string with the filtered options
    let filteredPubOptionList = filteredOptions.map(option => option.outerHTML).join('\n');
    let specItemArea = document.getElementById("spec-item-" + index);
    let innerHtml = document.getElementById("spec-item-" + index).innerHTML;

    let specItemEle = document.getElementById("spec-item-" + index);
    let specItems = getChildNodeList(specItemEle);
    let specLastItemId = specItems[specItems.length - 1].id;
    let newItemIdx = parseInt(specLastItemId.charAt(specLastItemId.length - 1)) + 1;

    innerHtml += `<div id="ad-spec-item-` + index + `-` + newItemIdx + `" class="c-ad-spec-item">
                            <div class="c-ad-spec-label">Select Your Publication:</div>
                            
                            <div class="select-publication">
                                <select class="form-control" id="select-pub-` + index + `-` + newItemIdx + `">
                                    ` + filteredPubOptionList + `
                                </select>

                                <button onclick="showAdItemModal(` + index + `, 0, getSelectedPublicationId('select-pub-` + index + `-0'))" data-target="#create-ad" data-toggle="modal">
                                            + Start An Ad For This Publication
                                </button>

                                <h4 class="black">$<span id="pub-price-` + index + `-` + newItemIdx + `">0.00</span></h4>
                                
                                <div id="pub-del-` + index + `-` + newItemIdx + `" class="pub-del" 
                                    onclick="deletePublication(` + index + `, ` + newItemIdx + `)">
                                    <i class="fa fa-trash"></i>
                                </div>
                            </div>

                            <hr class="black">

                            <div id="edit-ad-` + index + `-` + newItemIdx + `" class="edit-ad">
                                
                            </div>
                        </div>`;

    specItemArea.innerHTML = innerHtml;
}

// function showAdItemModal(demo, pub,pub_id) {
//     demo_index = demo;
//     pub_index = pub;
//     editAdFlag = false;

//     document.getElementById("ad-name").value = "";
//     document.getElementById("ad-type").value = "";
//     document.getElementById("ad-size").value = "";
//     document.getElementById("ad-rate").value = "";
//     document.getElementById("adjustment-value").innerHTML = "";
//     const selectedDates = [];
        
//     // Get all selected dates from the list
//     const dateItems = document.querySelectorAll('#selectedDatesList .list-group-item:not(.active) span:first-child');
//     dateItems.forEach(item => {
//         const formattedDate = new Date(item.textContent).toISOString().split('T')[0];
//         selectedDates.push(formattedDate);
//     });
//     selectedAdjustmentArray = [];
//     let selectedAdjustmentList = Array.from(document.querySelectorAll(".adjustment-select"))

//     selectedAdjustmentList.forEach(row => {
//         row.style.visibility = "hidden";
//     });
//        // Save the original unfiltered options when the modal is first opened
//     if (!originalAdTypeOptions) {
//         const selectElement = document.getElementById("ad-type");
//         originalAdTypeOptions = selectElement.innerHTML;
//     }
//     if (!originalAdAdjustmentOptions) {
//         const selectElement = document.getElementById("adjustment-row");
//         originalAdAdjustmentOptions = selectElement.innerHTML;
//     }

//     // Filter the dropdown options based on selected pub_id
//     const selectElement = document.getElementById("ad-type");
//     const options = selectElement.querySelectorAll('option');
//     const optionsAdjustment = document.getElementById("adjustment-row").querySelectorAll('.adjustment-item');
//     options.forEach(option => {
//         if (option.getAttribute('data-publication-id') !== pub_id) {
//             option.style.display = 'none';
//         } else {
//             option.style.display = 'block';
//         }
//     });
//     optionsAdjustment.forEach(option => {
//         if (option.getAttribute('data-publication-id') !== pub_id) {
//             option.style.display = 'none';
//         } else {
//             option.style.display = 'block';
//         }
//     });
// }

function resetDropdownOnClose() {
    const selectElement = document.getElementById("ad-type");
    const selectElementAdjustment = document.getElementById("adjustment-row");

    if (originalAdTypeOptions) {
        selectElement.innerHTML = originalAdTypeOptions;
    }
    if (originalAdAdjustmentOptions) {
        selectElementAdjustment.innerHTML = originalAdAdjustmentOptions;
    }
}

function updatePublicationPrice (event, demo, pub, ad) {
    const key = event.key;

    if (key !== "Enter")
        return;

    let count = document.getElementById("ad-count-" + demo + "-" + pub + "-" + ad).value

    if (isNaN(count))
        return;

    let elePubPrice = document.getElementById("pub-price-" + demo + "-" + pub);
    let pubPrice = "0.00";

    let adListEle = document.getElementById("edit-ad-" + demo + "-" + pub);
    let adList = getChildNodeList(adListEle);

    for (let i = 0; i < adList.length; i ++) {
        let adItemId = adList[i].id;
        let adItemIndex = adItemId.charAt(adItemId.length - 1);

        let unitPrice = document.getElementById("ad-unit-price-" + demo + "-" + pub + "-" + adItemIndex).innerText;
        let count = document.getElementById("ad-count-" + demo + "-" + pub + "-" + adItemIndex).value;

        let adjustmentEle = document.getElementById("adjustment-item-" + demo + "-" + pub + "-" + adItemIndex);
        let adjustmentList = getChildNodeList(adjustmentEle);

        let adjustmentPrice = 0;
        for (let j = 0; j < adjustmentList.length; j ++) {
            let adjustmentItem = adjustmentList[j];
            let adjustmentAmount = adjustmentItem.querySelector("#adj-amount").innerHTML.slice(1);

            adjustmentPrice += parseInt(adjustmentAmount);
        }

        pubPrice = parseFloat(pubPrice) + parseFloat(count) * parseFloat(unitPrice) + adjustmentPrice;
    }

    elePubPrice.innerHTML = pubPrice;
}

function updateTotal(demo_index) {
    let specEle = document.getElementById("spec-item-" + demo_index);
    let specList = getChildNodeList(specEle);

    let printAdPriceEle = document.getElementById("print-ad-price-" + demo_index);
    let printAdjPriceEle = document.getElementById("print-adj-price-" + demo_index);

    let printAdPrice = 0;
    let printAdjPrice = 0;

    for (let i = 0; i < specList.length; i ++) {
        let tempSpecId = specList[i].id;
        let tempSpecIdx = tempSpecId.charAt(tempSpecId.length - 1);

        // calculate the adjustments price
        let pubItem = document.getElementById("edit-ad-" + demo_index + "-" + tempSpecIdx);
        let pubItemList = getChildNodeList(pubItem);

        let adPrice = 0;
        let adjAmount = 0;
        for (let j = 0; j < pubItemList.length; j ++) {
            let tempId = pubItemList[j].id;
            let tempIdx = tempId.charAt(tempId.length - 1);

            let count = document.getElementById("ad-count-" + demo_index + "-" + tempSpecIdx + "-" + tempIdx).value;
            let adPrice = parseInt(document.getElementById("ad-unit-price-" + demo_index + "-" + tempSpecIdx + "-" + tempIdx).innerText);
            adPrice = parseInt(count) * adPrice;

            printAdPrice += adPrice;

            let adjItemElement = document.querySelector("#adjustment-item-" + demo_index + "-" + tempSpecIdx + "-" + tempIdx);
            let adjItemElementList = getChildNodeList(adjItemElement);

            for (let adj_idx = 0; adj_idx < adjItemElementList.length; adj_idx ++) {
                let temp = document.getElementById("ad-adj-item-" + demo_index + "-" + tempSpecIdx + "-" + tempIdx + "-" + adj_idx);
                let tempAmount = temp.querySelector("#adj-amount").innerText;
                adjAmount = adjAmount + parseFloat(tempAmount.replace(/\$/g, ""));
            }
        }

        printAdjPrice += adjAmount;
    }

    printAdPriceEle.innerText = printAdPrice.toString();
    printAdjPriceEle.innerText = printAdjPrice.toString();
    document.getElementById("print-total-price-" + demo_index).innerText = (printAdPrice + printAdjPrice).toString();
}

function filterAdFormats() {
    let adFormatEle = document.getElementById("ad-format");
    let adFormatChildArray = Array.from(adFormatEle.children);

    let adArray = [];
    adFormatChildArray.forEach(row => {
      let adName = row.querySelector('.pub_name').innerText;
      let adId = row.querySelector('.pub_name').id;
      let startIdx = adId.indexOf('_') + 1;
      adId = adId.substring(startIdx, adId.length);

      adArray.push({id: adId, name: adName});
    })

    adArray.sort((a, b) => {
      let nameA = a.name.toLowerCase();
      let nameB = b.name.toLowerCase();

      if (nameA < nameB) {
        return -1; // a should come before b
      }
      if (nameA > nameB) {
        return 1; // a should come after b
      }
      return 0; // names are equal
    });

    let adFormatHtml = "";
    for (let i = 0; i < adArray.length; i ++) {
        let temp = adArray[i];
        adFormatHtml += `<div id="ad_` + temp['id'] + `" class="col-md-4 pub_ele">
                                <div class="flex-col pub-card">
                                    <div class="c-ad-name">
                                        <h3 id="adTypeName_` + temp['id'] + `" class="pub_name">` + temp['name'] + `</h3>
                                    </div>

                                    <div class="flex-row content-left c-ml-10" onclick="selectStar(` + temp['id'] + `)">
                                        <img id="star_` + temp['id'] + `" src="/static/svg/Star-white.svg" style="height: 18px;">&nbsp;

                                        <h4 class="c-favorite" style="line-height: 20px;">Add to Favorites</h4>
                                    </div>

                                    <div class="c-adType-hover" onclick="selectAdFormat(` + temp['id'] + `)">
                                        Added to <br> Campaign!
                                    </div>
                                </div>

                                <div id="favoriteIcon_` + temp['id'] + `" class="text-center pub-mark">
                                    <img src="/static/svg/Vector (2).svg" style="height: 15px; margin-top:8px;">
                                </div>
                            </div>`;
    }

    adFormatEle.innerHTML = adFormatHtml;
}

// const getCookie = name => {
//     let cookie = {};
//     document.cookie.split(';').forEach(function (el) {
//         let [k, v] = el.split('=');
//         cookie[k.trim()] = v;
//     })
//     return cookie[name];
// }

// function getCampaignDetail() {
//     let campaignDetailEle = document.getElementById("sum-ad-details");
//     let campaignDetailList = getChildNodeList(campaignDetailEle);

//     let campaignArray = [];
//     for (let demo_idx = 0; demo_idx < campaignDetailList.length; demo_idx ++) {
//         let campaignName = selectedAdFormatsName[demo_idx];
//         let subAdPrice = document.getElementById("sum-print-ad-price-" + demo_idx).innerText;
//         let subAdjPrice = document.getElementById("sum-print-adj-price-" + demo_idx).innerText;
//         let subTotalPrice = document.getElementById("sum-print-total-price-" + demo_idx).innerText;
//         let pubArray = [];

//         let cdPubEle = document.getElementById("sum-spec-item-" + demo_idx);
//         let cdPubList = getChildNodeList(cdPubEle);
//         for (let pub_idx = 0; pub_idx < cdPubList.length; pub_idx ++) {
//             let tempPubId = cdPubList[pub_idx].id;
//             let tempPubIndex = tempPubId.charAt(tempPubId.length - 1);

//             let pubName = document.getElementById("sum-select-pub-" + demo_idx + "-" + tempPubIndex).innerText;
//             let pubPrice = document.getElementById("sum-pub-price-" + demo_idx + "-" + tempPubIndex).innerText;
//             let adArray = [];

//             let cdAdEle = document.getElementById("sum-edit-ad-" + demo_idx + "-" + tempPubIndex);
//             let dAdList = getChildNodeList(cdAdEle);
//             for (let ad_idx = 0; ad_idx < dAdList.length; ad_idx ++) {
//                 let tempId = dAdList[ad_idx].id;
//                 let tempAdIdx = tempId.charAt(tempId.length - 1);

//                 let adName = document.getElementById("sum-ad-name-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
//                 let adCount = document.getElementById("sum-ad-count-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
//                 let adPrice = document.getElementById("sum-ad-unit-price-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
//                 let adType = document.getElementById("sum-ad-type-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
//                 let adSize = document.getElementById("sum-ad-size-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
//                 let adRate = document.getElementById("sum-ad-rate-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
//                 let adBrief = document.getElementById("sum-ad-brief-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx).innerText;
//                 let adjArray = [];
//                 const selectedDates = [];
        
//                 // Get the selected month and year from the dropdowns
//                 const year = document.getElementById('year-selector').value;
//                 const month = document.getElementById('month-selector').value;
                
//                 // Background color indicating selected dates (update as needed)
//                 const selectedBackgroundColor = 'rgb(50, 115, 246)';
//                 let adCalendar = "#ad-calender"+ demo_idx + "-" + tempPubIndex + "-" + tempAdIdx
//                 // Get all <td> elements in the calendar
//                 const cells = document.querySelectorAll(`#calendar td`);
                
//                 cells.forEach(cell => {
//                     // Check if the background color matches the selected color
//                     if (cell.style.backgroundColor === selectedBackgroundColor && !cell.classList.contains('other-month')) {
//                         const dateText = cell.textContent.trim();
                        
//                         // Format the date to YYYY-MM-DD
//                         const formattedDate = `${year}-${month.padStart(2, '0')}-${dateText.padStart(2, '0')}`;
//                         selectedDates.push(formattedDate);
//                     }
//                 });
//                 let cdAdjEle = document.getElementById("sum-adjustment-item-" + demo_idx + "-" + tempPubIndex + "-" + tempAdIdx);
//                 let cdAdjList = getChildNodeList(cdAdjEle);
//                 for (let adj_idx = 0; adj_idx < cdAdjList.length; adj_idx ++) {
//                     let adjItem = cdAdjList[adj_idx];
//                     let adjName = adjItem.querySelector("#sum-ad-adj-code").innerText;
//                     let adjAmount = adjItem.querySelector("#sum-ad-adj-amount").innerText;

//                     adjArray.push({
//                         adjName: adjName,
//                         adjAmount: adjAmount
//                     });
//                 }

//                 adArray.push({
//                     adName: adName,
//                     adCount: adCount,
//                     adPrice: adPrice,
//                     adType: adType,
//                     adSize: adSize,
//                     adRate: adRate,
//                     adBrief: adBrief,
//                     adjArray: adjArray,
//                     adDates:selectedDates,
//                 });
//             }

//             pubArray.push({
//                 pubName: pubName,
//                 pubPrice: pubPrice,
//                 adArray: adArray
//             })
//         }

//         campaignArray.push({
//             campaignName: campaignName,
//             subAdPrice: subAdPrice,
//             subAdjPrice: subAdjPrice,
//             subTotalPrice: subTotalPrice,
//             pubArray: pubArray,
//         })
//     }
//     console.log(campaignArray);
//     return campaignArray;
// }

function summary_next() {
    const data = {
        campaignName: document.getElementById("sum-campaign-name").innerText,
        startDate: document.getElementById("sum-start-date").innerText,
        endDate: document.getElementById("sum-end-date").innerText,
        brief: document.getElementById("sum-brief").innerText,
        advertiserName: document.getElementById("sum-advertiser-name").innerText,
        advertiserId: document.getElementById("sum-advertiser-id").innerText,
        salesName: document.getElementById("sum-sales-name").innerText,
        salesId: document.getElementById("sum-sales-id").innerText,
        printTotal: document.getElementById("sum-print-total").innerText,
        adjTotal: document.getElementById("sum-adj-total").innerText,
        campaignTotal: document.getElementById("sum-campaign-total").innerText,
        campaignDetail: getCampaignDetail()
    }

    fetch('/advertising/classifieds/registerCampaign', {
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
        storedID = data.id;
        $.toastr.success('Saved Success');
    })
    .catch(error => {
        $.toastr.error("Saved failure");
    });

    showSection(6);
}

function viewCampaign() {
    window.location.href = `/advertising/classifieds/detail/?campaignId=${storedID}`;
}

// function editAdItem(demo, pub, ad) {
//     editAdSel = ad;

//     let adName = document.getElementById("ad-name-" + demo + "-" + pub + "-" + ad).innerText;
//     let adType = document.getElementById("ad-type-" + demo + "-" + pub + "-" + ad).innerText;
//     let adSize = document.getElementById("ad-size-" + demo + "-" + pub + "-" + ad).innerText;
//     let adRate = document.getElementById("ad-rate-" + demo + "-" + pub + "-" + ad).innerText;
//     let adBrief = document.getElementById("ad-brief-" + demo + "-" + pub + "-" + ad).innerText;

//     let adAdjEle = document.getElementById("adjustment-item-" + demo + "-" + pub + "-" + ad);
//     let adAdjList = getChildNodeList(adAdjEle);

//     let innerHtml = "";
//     selectedAdjustmentArray = [];
//     for (let m = 0; m < adAdjList.length; m ++) {
//         let adjItem = adAdjList[m];

//         let code = adjItem.querySelector("#adj-name").innerText;
//         let amount = adjItem.querySelector("#adj-amount").innerText;
//         let id = adjItem.querySelector("#adj-id").value;

//         innerHtml += `<div id="adjustments_list-` + id + `" class="mt-1 flex-row sel-adjustment">
//                         <h5 id="ad-adj-code" class="black">` + code + `</h5>
//                         <h5 id="ad-adj-amount" class="black">` + amount + `</h5>
//                         <input id="ad-adj-id" type="hidden" value="` + id + `">
//                       </div>`;

//         selectedAdjustmentArray.push(id);

//         document.getElementById("adjustment-select-" + id).style.visibility = "visible";
//     }

//     let adRateId = "";

//     for (let i = 0; i < ratingList.length; i ++) {
//         let item = ratingList[i];

//         if (item.fields['name'] === adRate) {
//             adRateId = item.pk;
//         }
//     }

//     document.getElementById("ad-name").value = adName;
//     document.getElementById("ad-type").value = adType;
//     document.getElementById("ad-size").value = adSize;
//     document.getElementById("ad-rate").value = adRateId;
//     document.getElementById("ad-brief").value = adBrief;
//     document.getElementById("adjustment-value").innerHTML = innerHtml;

//     editAdFlag = true;
// }

function deleteAdItem(demo, pub, ad) {
    let parentItem = document.getElementById("edit-ad-" + demo + "-" + pub);
    let removeItem = document.getElementById("edit-ad-item-" + demo + "-" + pub + "-" + ad);

    parentItem.removeChild(removeItem);

    getUpdatedPublicationTotalPrice(demo, pub);
}

function deletePublication(demo, pub) {
    let publicationEle = document.getElementById("spec-item-" + demo);
    let selPublication = document.getElementById("ad-spec-item-" + demo + "-" + pub);

    publicationEle.removeChild(selPublication);
}

$.toastr.config({
    time: 3000,
    position: "top-center"
});

function drawCalendar() {
  var today = moment();

  function getPerpetualCalendar(year, month) {
    const daysOfWeek = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
    const firstDayOfMonth = moment([year, month - 1, 1]);
    const lastDayOfMonth = moment([year, month, 0]);
    const daysInMonth = lastDayOfMonth.date();
    const firstDayOfWeek = firstDayOfMonth.day();

    let calendarHTML = '<table>';
    calendarHTML += '<tr>';
    
    for (let i = 0; i < daysOfWeek.length; i++) {
      calendarHTML += '<th>' + daysOfWeek[i] + '</th>';
    }
    
    calendarHTML += '</tr>';

    let dayCounter = 1;

    for (let i = 0; i < 6; i++) {
      calendarHTML += '<tr>';

      for (let j = 0; j < 7; j++) {
        const dayValue = i * 7 + j + 1 - firstDayOfWeek;
        const isPrevMonthDay = dayValue <= 0;
        const isNextMonthDay = dayValue > daysInMonth;
        if (i === 0 && j < firstDayOfWeek) {
          const prevMonthDays = moment([year, month - 2, 1]).endOf('month').date();
          calendarHTML += '<td class="other-month">' + (prevMonthDays - (firstDayOfWeek - 1) + j) + '</td>';
        } else if (dayCounter > daysInMonth) {
          calendarHTML += '<td class="other-month">' + (dayCounter - daysInMonth) + '</td>';
          dayCounter++;
        } else {
          const isSelected = isDateSelected(year, month, dayCounter);
          const backgroundColor = isSelected ? 'rgb(50, 115, 246)' : '';
          const tooltipText = getTooltipText(year, month, dayCounter);

          calendarHTML += '<td style="background-color: ' + backgroundColor + ';">' + dayCounter + '</td>';
          dayCounter++;
        }
      }

      calendarHTML += '</tr>';
    }

    calendarHTML += '</table>';
    return calendarHTML;
  }

  const year = today.year();
  const month = today.month() + 1; // Months are 0-indexed in moment.js
  const perpetualCalendar = getPerpetualCalendar(year, month);

  // Display the calendar in an HTML element with id "calendar-container"
  document.getElementById("ad-calendar").innerHTML = perpetualCalendar;

  document.getElementById('ad-prev-month-btn').addEventListener('click', showPreviousMonth);
  document.getElementById('ad-next-month-btn').addEventListener('click', showNextMonth);
  document.getElementById('ad-month-selector').addEventListener('change', showSelectedMonth);
  document.getElementById('ad-year-selector').addEventListener('change', showSelectedYear);

  // Function to populate month and year selectors
  function populateSelectors() {
    const monthSelector = document.getElementById('ad-month-selector');
    const yearSelector = document.getElementById('ad-year-selector');
    const months = moment.months();
    const currentYear = moment().year();
    const years = Array.from({ length: 10 }, (_, i) => currentYear - 5 + i); // Adjust the range as needed

    months.forEach((month, index) => {
      const option = document.createElement('option');
      option.value = index + 1;
      option.textContent = month;
      monthSelector.appendChild(option);
    });

    years.forEach((year) => {
      const option = document.createElement('option');
      option.value = year;
      option.textContent = year;
      yearSelector.appendChild(option);
    });

    // Set initial values
    monthSelector.value = moment().month() + 1;
    yearSelector.value = currentYear;
  }

  // Function to show the previous month
  function showPreviousMonth() {
    const monthSelector = document.getElementById('ad-month-selector');
    const currentMonth = parseInt(monthSelector.value, 10);
    const newMonth = currentMonth === 1 ? 12 : currentMonth - 1;
    const newYear = currentMonth === 1 ? parseInt(document.getElementById('ad-year-selector').value, 10) - 1 : parseInt(document.getElementById('ad-year-selector').value, 10);
    monthSelector.value = newMonth;
    document.getElementById('ad-year-selector').value = newYear;
    // Update your calendar with the new month and year
    const perpetualCalendar = getPerpetualCalendar(newYear, newMonth);
    document.getElementById("ad-calendar").innerHTML = perpetualCalendar;
  }

  // Function to show the next month
  function showNextMonth() {
    const monthSelector = document.getElementById('ad-month-selector');
    const currentMonth = parseInt(monthSelector.value, 10);
    const newMonth = currentMonth === 12 ? 1 : currentMonth + 1;
    const newYear = currentMonth === 12 ? parseInt(document.getElementById('ad-year-selector').value, 10) + 1 : parseInt(document.getElementById('ad-year-selector').value, 10);
    monthSelector.value = newMonth;
    document.getElementById('ad-year-selector').value = newYear;
    // Update your calendar with the new month and year
    const perpetualCalendar = getPerpetualCalendar(newYear, newMonth);
    document.getElementById("ad-calendar").innerHTML = perpetualCalendar;
  }

  // Function to show the selected month
  function showSelectedMonth() {
    const selectedMonth = parseInt(document.getElementById('ad-month-selector').value, 10);
    const selectedYear = parseInt(document.getElementById('ad-year-selector').value, 10);
    // Update your calendar with the selected month and year
    const perpetualCalendar = getPerpetualCalendar(selectedYear, selectedMonth);
    document.getElementById("ad-calendar").innerHTML = perpetualCalendar;
  }

  // Function to show the selected year
  function showSelectedYear() {
    const selectedYear = parseInt(document.getElementById('ad-year-selector').value, 10);
    const selectedMonth = parseInt(document.getElementById('ad-month-selector').value, 10);
    // Update your calendar with the selected month and year
    const perpetualCalendar = getPerpetualCalendar(selectedYear, selectedMonth);
    document.getElementById("ad-calendar").innerHTML = perpetualCalendar;
  }

  function isDateSelected(year, month, day) {
    return selectedDates.some(date => date.year === year && date.month === month && date.day === day);
  }

  function selectDate(year, month, day) {
    const index = selectedDates.findIndex(date => date.year === year && date.month === month && date.day === day);

    if (index === -1) {
      // Not selected, add to the array
      selectedDates.push({ year, month, day, adsBooked: 5 }); // You can set the initial value for adsBooked here
    } else {
      // Already selected, remove from the array
      selectedDates.splice(index, 1);
    }

    // Update the calendar with the new selection
    const perpetualCalendar = getPerpetualCalendar(year, month);
    document.getElementById("ad-calendar").innerHTML = perpetualCalendar;
  }

  function getTooltipText(year, month, day) {
    const selectedDate = selectedDates.find(date => date.year === year && date.month === month && date.day === day);

    if (selectedDate) {
      const numAdsBooked = selectedDate.adsBooked || 0;
      return numAdsBooked + ' ad' + (numAdsBooked !== 1 ? 's' : '') + ' have been booked';
    }

    return '';
  }

  document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('ad-calendar').addEventListener('click', function(event) {
      if (event.target.tagName === 'TD') {
        const dayValue = parseInt(event.target.textContent, 10);
        selectDate(parseInt(document.getElementById('ad-year-selector').value, 10), parseInt(document.getElementById('ad-month-selector').value, 10), dayValue);
      }
    });
  });

  // Call the function to populate selectors initially
  populateSelectors();
}

function drawadCalendar() {
    var today = moment();
  
    function getPerpetualCalendar(year, month) {
      const daysOfWeek = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
      const firstDayOfMonth = moment([year, month - 1, 1]);
      const lastDayOfMonth = moment([year, month, 0]);
      const daysInMonth = lastDayOfMonth.date();
      const firstDayOfWeek = firstDayOfMonth.day();
  
      let calendarHTML = '<table>';
      calendarHTML += '<tr>';
      
      for (let i = 0; i < daysOfWeek.length; i++) {
        calendarHTML += '<th>' + daysOfWeek[i] + '</th>';
      }
      
      calendarHTML += '</tr>';
  
      let dayCounter = 1;
  
      for (let i = 0; i < 6; i++) {
        calendarHTML += '<tr>';
  
        for (let j = 0; j < 7; j++) {
          const dayValue = i * 7 + j + 1 - firstDayOfWeek;
          const isPrevMonthDay = dayValue <= 0;
          const isNextMonthDay = dayValue > daysInMonth;
          if (i === 0 && j < firstDayOfWeek) {
            const prevMonthDays = moment([year, month - 2, 1]).endOf('month').date();
            calendarHTML += '<td class="other-month">' + (prevMonthDays - (firstDayOfWeek - 1) + j) + '</td>';
          } else if (dayCounter > daysInMonth) {
            calendarHTML += '<td class="other-month">' + (dayCounter - daysInMonth) + '</td>';
            dayCounter++;
          } else {
            const isSelected = isDateSelected(year, month, dayCounter);
            const backgroundColor = isSelected ? 'rgb(50, 115, 246)' : '';
            const tooltipText = getTooltipText(year, month, dayCounter);
  
            calendarHTML += '<td style="background-color: ' + backgroundColor + ';">' + dayCounter + '</td>';
            dayCounter++;
          }
        }
  
        calendarHTML += '</tr>';
      }
  
      calendarHTML += '</table>';
      return calendarHTML;
    }
  
    const year = today.year();
    const month = today.month() + 1; // Months are 0-indexed in moment.js
    const perpetualCalendar = getPerpetualCalendar(year, month);
  
    // Display the calendar in an HTML element with id "calendar-container"
    document.getElementById("ad-sum-calendar").innerHTML = perpetualCalendar;
  
    document.getElementById('ad-sum-prev-month-btn').addEventListener('click', showPreviousMonth);
    document.getElementById('ad-sum-next-month-btn').addEventListener('click', showNextMonth);
    document.getElementById('ad-sum-month-selector').addEventListener('change', showSelectedMonth);
    document.getElementById('ad-sum-year-selector').addEventListener('change', showSelectedYear);
  
    // Function to populate month and year selectors
    function populateSelectors() {
      const monthSelector = document.getElementById('ad-sum-month-selector');
      const yearSelector = document.getElementById('ad-sum-year-selector');
      const months = moment.months();
      const currentYear = moment().year();
      const years = Array.from({ length: 10 }, (_, i) => currentYear - 5 + i); // Adjust the range as needed
  
      months.forEach((month, index) => {
        const option = document.createElement('option');
        option.value = index + 1;
        option.textContent = month;
        monthSelector.appendChild(option);
      });
  
      years.forEach((year) => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelector.appendChild(option);
      });
  
      // Set initial values
      monthSelector.value = moment().month() + 1;
      yearSelector.value = currentYear;
    }
  
    // Function to show the previous month
    function showPreviousMonth() {
      const monthSelector = document.getElementById('ad-sum-month-selector');
      const currentMonth = parseInt(monthSelector.value, 10);
      const newMonth = currentMonth === 1 ? 12 : currentMonth - 1;
      const newYear = currentMonth === 1 ? parseInt(document.getElementById('ad-sum-year-selector').value, 10) - 1 : parseInt(document.getElementById('ad-sum-year-selector').value, 10);
      monthSelector.value = newMonth;
      document.getElementById('ad-sum-year-selector').value = newYear;
      // Update your calendar with the new month and year
      const perpetualCalendar = getPerpetualCalendar(newYear, newMonth);
      document.getElementById("ad-sum-calendar").innerHTML = perpetualCalendar;
    }
  
    // Function to show the next month
    function showNextMonth() {
      const monthSelector = document.getElementById('ad-sum-month-selector');
      const currentMonth = parseInt(monthSelector.value, 10);
      const newMonth = currentMonth === 12 ? 1 : currentMonth + 1;
      const newYear = currentMonth === 12 ? parseInt(document.getElementById('ad-sum-year-selector').value, 10) + 1 : parseInt(document.getElementById('ad-sum-year-selector').value, 10);
      monthSelector.value = newMonth;
      document.getElementById('ad-sum-year-selector').value = newYear;
      // Update your calendar with the new month and year
      const perpetualCalendar = getPerpetualCalendar(newYear, newMonth);
      document.getElementById("ad-sum-calendar").innerHTML = perpetualCalendar;
    }
  
    // Function to show the selected month
    function showSelectedMonth() {
      const selectedMonth = parseInt(document.getElementById('ad-sum-month-selector').value, 10);
      const selectedYear = parseInt(document.getElementById('ad-sum-year-selector').value, 10);
      // Update your calendar with the selected month and year
      const perpetualCalendar = getPerpetualCalendar(selectedYear, selectedMonth);
      document.getElementById("ad-sum-calendar").innerHTML = perpetualCalendar;
    }
  
    // Function to show the selected year
    function showSelectedYear() {
      const selectedYear = parseInt(document.getElementById('ad-sum-year-selector').value, 10);
      const selectedMonth = parseInt(document.getElementById('ad-sum-month-selector').value, 10);
      // Update your calendar with the selected month and year
      const perpetualCalendar = getPerpetualCalendar(selectedYear, selectedMonth);
      document.getElementById("ad-sum-calendar").innerHTML = perpetualCalendar;
    }
  
    function isDateSelected(year, month, day) {
      return selectedDates.some(date => date.year === year && date.month === month && date.day === day);
    }
  
    function selectDate(year, month, day) {
      const index = selectedDates.findIndex(date => date.year === year && date.month === month && date.day === day);
  
      if (index === -1) {
        // Not selected, add to the array
        selectedDates.push({ year, month, day, adsBooked: 5 }); // You can set the initial value for adsBooked here
      } else {
        // Already selected, remove from the array
        selectedDates.splice(index, 1);
      }
  
      // Update the calendar with the new selection
      const perpetualCalendar = getPerpetualCalendar(year, month);
      document.getElementById("ad-sum-calendar").innerHTML = perpetualCalendar;
    }
  
    function getTooltipText(year, month, day) {
      const selectedDate = selectedDates.find(date => date.year === year && date.month === month && date.day === day);
  
      if (selectedDate) {
        const numAdsBooked = selectedDate.adsBooked || 0;
        return numAdsBooked + ' ad' + (numAdsBooked !== 1 ? 's' : '') + ' have been booked';
      }
  
      return '';
    }
  
    document.addEventListener('DOMContentLoaded', function() {
      document.getElementById('ad-sum-calendar').addEventListener('click', function(event) {
        if (event.target.tagName === 'TD') {
          const dayValue = parseInt(event.target.textContent, 10);
          selectDate(parseInt(document.getElementById('ad-sum-year-selector').value, 10), parseInt(document.getElementById('ad-sum-month-selector').value, 10), dayValue);
        }
      });
    });
  
    // Call the function to populate selectors initially
    populateSelectors();
    
  }

