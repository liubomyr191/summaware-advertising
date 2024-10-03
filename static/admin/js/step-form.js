function getCookie(name) {
  let cookie = {};
  document.cookie.split(';').forEach(function (el) {
      let [k, v] = el.split('=');
      cookie[k.trim()] = v;
  })
  return cookie[name];
}
function next_step(event, type, step_name=null, data=null) {
  // Prevent the default button action if needed
  event.preventDefault();

  // Get the button that triggered the function
  var button = event.target;
  var parent = button.closest('.multistep-container');
  // Get the closest form section to the button
  var currentSection = button.closest('.multistep-content');

  // Ensure a valid current section is found
  if (!currentSection) {
    console.error('No active section found.');
    return;
  }

  // Find all required inputs in the current section
  var requiredInputs = currentSection.querySelectorAll('[required]');
  var allFilled = true;

  // Check if all required inputs are filled
  requiredInputs.forEach(function (input) {
    if (!input.value.trim()) {
      allFilled = false;
      input.classList.add('input-error'); // Optionally, add an error class for styling
    } else {
      input.classList.remove('input-error'); // Remove error class if input is filled
    }
  });

  // If not all required inputs are filled, exit the function
  if (!allFilled) {
    alert('Please fill in all required fields.');
    return;
  }

  var nextSection = null;
  // Find the next section
  if (step_name === null) {
    nextSection = currentSection.nextElementSibling;
  } else {
    var parent = currentSection.closest('.c-card');
    var allSections = parent.querySelectorAll('.multistep-content');
    for (var i = 0; i < allSections.length; i++) {
      if (allSections[i] === currentSection && i < allSections.length - 1) {
        nextSection = allSections[i + 1];
        break;
      }
    }

  }

  // If there is no next section, exit the function
  if (!nextSection || !nextSection.classList.contains('multistep-content')) return;

  // Remove the 'hide' class from the next section
  nextSection.classList.remove('hide');

  // Get all progress icons within the specified form
  var progressIcons = parent.querySelectorAll('.progress-icons > .progress-dot-container > div');

  // Find the index of the current active progress icon
  var currentIndex;
  progressIcons.forEach(function (icon, index) {
    if (icon.classList.contains('progress-active')) {
      currentIndex = index;
    }
  });

  // If the current index is valid and there is a next progress icon, add 'progress-active' class to it
  if (currentIndex !== undefined && progressIcons[currentIndex + 1]) {
    progressIcons[currentIndex + 1].classList.add('progress-active');
  }

  // Hide the current section
  currentSection.classList.add('hide');
  
  if (step_name !== null && data !== null) {
    fetch('advertising/create-style', {
      method: 'POST',
      body: JSON.stringify({
        step_name: step_name,
        data: data
      }),
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      }
    })
    .then(response => response.json())
    .then((response) => {
      if(response.success) {
        $.toastr.success("Progress Saved Successfully");
          
      } else {
        $.toastr.error("Save Failed");
      }
    })
    .catch((error) => {
      $.toastr.error("Save Failed");
      console.error(error);
    });
  }


  var type = button.id
  if(type == '') return;
  var product = document.querySelector(`.${type}`);
  if(type == 'magazine' || type == 'newspaper') {
    var product_mag = product.querySelector("#product-mag").value;
    var fold_orientation = product.querySelector("#orientation").value;
    var height = product.querySelector("#height").value;
    var width = product.querySelector("#width").value;
    var columns = product.querySelector("#columns").value;
    var page_height = product.querySelector("#page-height").value;
    var page_border = product.querySelector("#page-border").value;
    var gutter_size = product.querySelector("#gutter-size").value;
    document.querySelector('.review-product-mag').textContent = product_mag;
    document.querySelector('.review-orientation').textContent = fold_orientation;
    document.querySelector('.review-size').textContent = `${height} * ${width}`;
    document.querySelector('.review-columns').textContent = columns;
    document.querySelector('.review-page-height').textContent = page_height;
    document.querySelector('.review-page-border').textContent = page_border;
    document.querySelector('.review-gutter-size').textContent = gutter_size;
  } else if(type == 'digital') {
    var product_mag = product.querySelector("#product-mag").value;
    var format = product.querySelector("#format").value;
    var ad_type = product.querySelector("#ad-type").value;
    var height = product.querySelector("#height").value;
    var width = product.querySelector("#width").value;
    document.querySelector('.review-product-mag').textContent = product_mag;
    document.querySelector('.review-format').textContent = format;
    document.querySelector('.review-ad-type').textContent = ad_type;
    document.querySelector('.review-size').textContent = `${height} * ${width}`;
  }
  if(type == 'review-newspaper' || type == 'review-magazine' || type == 'review-digital') {
    let form = $(`#${type.split('-')[1]}-standardsize-table`);
    var formData = new FormData(form[0]);
    let data = {};
    var tbody = document.getElementById('review-standardsize-table-body');
    tbody.innerHTML = '';
    for (const [key, value] of formData) {
        data[key] = value;
        var id = key.split('-');
        id = id[0];
        if(value == 'active') {
          var trElement = document.querySelector(`tr[data-index="${id}"]`);
          var newRow = '<tr>';
          if (trElement) {
            const tdElements = trElement.querySelectorAll('td');
            var i = 0;
            tdElements.forEach(td => {
                const tdData = td.textContent;
                if(i == 5) newRow += `<td>Active</td>`;
                else newRow += `<td>${tdData}</td>`;
                i++;
            });
          }
          newRow += '</tr>';
          
          tbody.insertAdjacentHTML('beforeend', newRow);
        }
    }
  }
}

function previous_step(event) {
  // Prevent the default button action if needed
  event.preventDefault();
  var button = event.target;
  var parent = button.closest('.multistep-container');
  // Get the current active section
  var currentSection = parent.querySelector('.multistep-content:not(.hide)');

  // Find the previous section
  var previousSection = currentSection.previousElementSibling;

  if (previousSection && previousSection.tagName.toLowerCase() === 'form') {
    previousSection = previousSection.firstElementChild;
  } else if (previousSection === null) {
    var parent = currentSection.closest('.c-card');
    var allSections = parent.querySelectorAll('.multistep-content');
    for (var i = 0; i < allSections.length; i++) {
      if (allSections[i] === currentSection && i > 0) {
        previousSection = allSections[i - 1];
        break;
      }
    }
  }
  if (!previousSection) return;

  // Remove the 'hide' class from the previous section
  previousSection.classList.remove('hide');

  // Get all progress icons
  var progressIcons = parent.querySelectorAll('.progress-icons > .progress-dot-container > div');

  // Find the index of the current active progress icon
  var currentIndex;
  progressIcons.forEach(function (icon, index) {
    if (icon.classList.contains('progress-active')) {
      currentIndex = index;
    }
  });

  // If the current index is valid and there is a previous progress icon, remove 'progress-active' class from it
  if (currentIndex !== undefined && progressIcons[currentIndex - 1]) {
    progressIcons[currentIndex].classList.remove('progress-active');
  }

  // Hide the current section
  currentSection.classList.add('hide');
}

function create_product(event, type) {
  var button = event.target;
  var parent = button.closest('.multistep-container');
  // Get the current active section
  var currentSection = parent.querySelector('.multistep-content:not(.hide)');

  // Find the last section
  var lastSection = parent.querySelector('.multistep-content:last-of-type');

  // If the current section is the last section, exit the function
  if (currentSection === lastSection) return;

  // Remove the 'hide' class from the last section
  lastSection.classList.remove('hide');

  // Get all progress icons
  var progressIcons = parent.querySelectorAll('.progress-icons > div');

  // Add the 'progress-active' class to the last progress icon
  progressIcons[progressIcons.length - 1].classList.add('progress-active');

  // Hide the current section
  currentSection.classList.add('hide');
  let data = {};
  var product = parent.querySelector(`.${type}`);
  console.log(product);
  const tbody = document.getElementById('review-standardsize-table-body');
  const rows = tbody.getElementsByTagName('tr');
  var sizes = [];
  for(var i = 0; i < rows.length; i++) {
    sizes.push(Number(rows[i].getElementsByTagName('td')[0].innerText));
  }
  if(type == 'magazine' || type == 'newspaper') {
    var product_mag = product.querySelector("#product-mag").value;
    var measurement_type = product.querySelector("#measurement-type").value;
    var fold_orientation = product.querySelector("#orientation").value;
    var height = product.querySelector("#height").value;
    var width = product.querySelector("#width").value;
    var columns = product.querySelector("#columns").value;
    var column_width = product.querySelector("#column-width").value;
    var page_width = product.querySelector("#page-width").value;
    var page_height = product.querySelector("#page-height").value;
    var page_border = product.querySelector("#page-border").value;
    var gutter_size = product.querySelector("#gutter-size").value;
    
    data = {
      product_mag : product_mag,
      measurement_type : measurement_type,
      fold_orientation : fold_orientation,
      height : height ? height : 0,
      width : width ? width : 0,
      columns : columns ? columns : 0,
      column_width : column_width ? column_width : 0,
      page_width : page_width ? page_width : 0,
      page_height : page_height ? page_height : 0,
      page_border : page_border ? page_border : 0,
      gutter_size : gutter_size ? gutter_size : 0,
      sizes: sizes,
    }
  } else {
    var product_mag = product.querySelector("#product-mag").value;
    var format = product.querySelector("#format").value;
    var ad_type = product.querySelector("#ad-type").value;
    var height = product.querySelector("#height").value;
    var width = product.querySelector("#width").value; 
    data = {
      product_mag : product_mag,
      format : format,
      adminadtype : ad_type,
      height : height ? height : 0,
      width : width ? width : 0,
      sizes: sizes,
    }
  }
  fetch(`/advertising/adadmin/financial/new-${type}`, {
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
      if(data.success == true) {
        $.toastr.success('Saved Success');
      } else {
        $.toastr.error('Saved Failure');
      }
  })
  .catch(error => {
      $.toastr.error("Saved failure");
  });
}

// Secondary Step Form
// Get all progress buttons
var progressButtons = document.querySelectorAll('.progress-btn');

// Loop through each button and add click event listener
progressButtons.forEach(function (button) {
  button.addEventListener('click', function () {
    // Remove 'active-step' class from all buttons
    progressButtons.forEach(function (btn) {
      btn.classList.remove('active-step');
    });

    // Add 'active-step' class to the clicked button
    this.classList.add('active-step');
  });
});

// Get all progress buttons and step form content divs
var progressButtons = document.querySelectorAll('.progress-btn');
var stepFormContents = document.querySelectorAll('.step-form-content');
var arrowButtons = document.querySelectorAll('.arrow');

// Function to move to the next step
function moveToNextStep() {
  // Find the index of the currently active step
  var currentIndex = Array.from(stepFormContents).findIndex(function (content) {
    return content.classList.contains('active');
  });

  // If there's a next step
  if (currentIndex < stepFormContents.length - 1) {
    // Remove 'active' class from current step
    stepFormContents[currentIndex].classList.remove('active');

    // Add 'hide' class to current step
    stepFormContents[currentIndex].classList.add('hide');

    // Show the next step
    stepFormContents[currentIndex + 1].classList.remove('hide');
    stepFormContents[currentIndex + 1].classList.add('active');

    // Update progress buttons
    progressButtons.forEach(function (button) {
      button.classList.remove('active-step');
    });
    progressButtons[currentIndex + 1].classList.add('active-step');
  }
}

// Function to move to the previous step
function moveToPreviousStep() {
  // Find the index of the currently active step
  var currentIndex = Array.from(stepFormContents).findIndex(function (content) {
    return content.classList.contains('active');
  });

  // If there's a previous step
  if (currentIndex > 0) {
    // Remove 'active' class from current step
    stepFormContents[currentIndex].classList.remove('active');

    // Add 'hide' class to current step
    stepFormContents[currentIndex].classList.add('hide');

    // Show the previous step
    stepFormContents[currentIndex - 1].classList.remove('hide');
    stepFormContents[currentIndex - 1].classList.add('active');

    // Update progress buttons
    progressButtons.forEach(function (button) {
      button.classList.remove('active-step');
    });
    progressButtons[currentIndex - 1].classList.add('active-step');
  }
}

// Add click event listeners to arrow buttons
arrowButtons[0].addEventListener('click', moveToPreviousStep); // Left arrow
arrowButtons[1].addEventListener('click', moveToNextStep); // Right arrow

// Add click event listeners to progress buttons
progressButtons.forEach(function (button, index) {
  button.addEventListener('click', function () {
    // Hide all step form contents
    stepFormContents.forEach(function (content) {
      content.classList.add('hide');
    });

    // Show the corresponding step form content
    stepFormContents[index].classList.remove('hide');
    stepFormContents[index].classList.add('active');

    // Remove 'active' class from the previous step form content
    if (index > 0) {
      stepFormContents[index - 1].classList.remove('active');
    }

    // Update progress buttons
    progressButtons.forEach(function (btn) {
      btn.classList.remove('active-step');
    });
    this.classList.add('active-step');
  });
});
