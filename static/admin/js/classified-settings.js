// $('.color-block').click(function () {
//   $(this).toggleClass('selected');
// });

// Hide CMYK on Select
document.getElementById('fontColorSelect').addEventListener('change', function () {
  var selectedValue = this.value;
  var colorsContainer = document.querySelector('.colors-container');

  if (selectedValue === 'spot-color') {
    colorsContainer.style.display = 'block';
  } else {
    colorsContainer.style.display = 'none';
  }
});

// Hide Solid Fill
document.getElementById('textOuline').addEventListener('change', function () {
  var selectedValue = this.value;
  var solidFillBtn = document.querySelector('.color-fill');

  if (selectedValue === 'solid-fill') {
    solidFillBtn.style.display = 'block';
  } else {
    solidFillBtn.style.display = 'none';
  }
});

// Text Outline Range Slider
document.addEventListener('DOMContentLoaded', function () {
  const rangeInput = document.getElementById('transparencyRange');
  const textInput = document.getElementById('transparencyText');

  // Function to update the text input with the value of the range input
  function updateTextInput() {
    textInput.value = rangeInput.value + '%';
  }

  // Function to update the range input with the value of the text input
  function updateRangeInput() {
    const value = parseInt(textInput.value);
    if (!isNaN(value)) {
      rangeInput.value = Math.max(Math.min(value, parseInt(rangeInput.max)), parseInt(rangeInput.min));
    }
  }

  // Event listeners to synchronize range and text inputs
  rangeInput.addEventListener('input', updateTextInput);
  textInput.addEventListener('input', updateRangeInput);
});

// Gradient Presets
document.addEventListener('DOMContentLoaded', function () {
  const gradientSelectorButton = document.getElementById('gradientSelector');
  const gradientMenu = document.querySelector('.dropdown-menu');

  gradientSelectorButton.addEventListener('click', function () {
    gradientMenu.style.display = gradientMenu.style.display === 'grid' ? 'none' : 'grid';
  });

  // Close dropdown menu when clicking outside of it
  document.addEventListener('click', function (event) {
    if (!gradientMenu.contains(event.target) && event.target !== gradientSelectorButton) {
      gradientMenu.style.display = 'none';
    }
  });
});

// Gradient Preset options
// Function to populate the dropdown menu with default gradient presets
const gradientPresets = {
  linear: [
    { name: 'Linear Gradient 1', value: 'linear-gradient(to right, #fff, #f1c40f)' },
    { name: 'Linear Gradient 2', value: 'linear-gradient(to left, #fff, #00FFFF)' },
    { name: 'Linear Gradient 3', value: 'linear-gradient(to bottom, #fff, #FF00FF)' },
    { name: 'Linear Gradient 4', value: 'linear-gradient(to bottom, #fff, #000000)' }
  ],
  radial: [
    { name: 'Radial Gradient 1', value: 'radial-gradient(#fff, #f1c40f)' },
    { name: 'Radial Gradient 2', value: 'radial-gradient(#fff, #00FFFF)' },
    { name: 'Radial Gradient 3', value: 'radial-gradient(#fff, #FF00FF)' },
    { name: 'Radial Gradient 3', value: 'radial-gradient(#fff, #000000)' }
  ],
  diagonal: [
    { name: 'Diagonal Gradient 1', value: 'linear-gradient(45deg, #fff, #f1c40f)' },
    { name: 'Diagonal Gradient 2', value: 'linear-gradient(45deg, #fff, #00FFFF)' },
    { name: 'Diagonal Gradient 3', value: 'linear-gradient(45deg, #fff, #FF00FF)' },
    { name: 'Diagonal Gradient 3', value: 'linear-gradient(45deg, #fff, #000000)' }
  ]
};

// Function to populate the dropdown menu with gradient presets based on selected type
function populateGradientPresets() {
  const gradientMenu = document.querySelector('.dropdown-menu');
  gradientMenu.innerHTML = ''; // Clear existing options

  const selectedType = document.getElementById('gradientType').value;
  const presets = gradientPresets[selectedType];

  presets.forEach(gradient => {
    const option = document.createElement('div');
    option.classList.add('dropdown-item');
    option.style.background = gradient.value; // Set background color to the gradient
    option.addEventListener('click', function () {
      applyGradientPreset(gradient.value);
    });
    gradientMenu.appendChild(option);
  });
}

// Function to apply the selected gradient preset
function applyGradientPreset(presetValue) {
  // Apply the selected gradient value to your element here
}

// Call the function to populate the dropdown with default presets
populateGradientPresets();

// Event listener to update presets when the select field changes
document.getElementById('gradientType').addEventListener('change', populateGradientPresets);

// Toggle Text Effects
var effectToggle = document.querySelectorAll('.effect-toggle');

// Loop through each button and add click event listener
effectToggle.forEach(function (button) {
  button.addEventListener('click', function () {
    // Remove 'active-step' class from all buttons
    effectToggle.forEach(function (btn) {
      btn.classList.remove('active');
    });

    // Add 'active-step' class to the clicked button
    this.classList.add('active');
  });
});

var effectContents = document.querySelectorAll('.effects-content');

// Add click event listeners to progress buttons
effectToggle.forEach(function (button, index) {
  button.addEventListener('click', function () {
    // Hide all step form contents
    effectContents.forEach(function (content) {
      content.classList.add('hide');
    });

    // Show the corresponding step form content
    effectContents[index].classList.remove('hide');
    effectContents[index].classList.add('active');

    // Remove 'active' class from the previous step form content
    if (index > 0) {
      effectContents[index - 1].classList.remove('active');
    }

    // Update progress buttons
    effectToggle.forEach(function (btn) {
      btn.classList.remove('active');
    });
    this.classList.add('active');
  });
});

$.fn.colorSelect = function () {
  function build($select) {
    var html = '';
    var listItems = '';

    $select.find('option').each(function () {
      listItems += '' + '<li style="background:' + this.value + '" data-colorVal="' + this.value + '">' + '<span>' + this.text + '</span>' + '</li>';
    });

    html = '' + '<div class="color-select">' + '<span>Select one</span>' + '<ul>' + listItems + '</ul>' + '</div>';

    return html;
  }

  this.each(function () {
    var $this = $(this);

    $this.hide();

    $this.after(build($this));
  });
};

$(document)
  .on('click', '.color-select > span', function () {
    $(this).siblings('ul').toggle();
  })
  .on('click', '.color-select li', function () {
    var $this = $(this);
    var color = $this.attr('data-colorVal');
    var colorText = $this.find('span').text();
    var $value = $this.parents('.color-select').find('span:first');
    var $select = $this.parents('.color-select').prev('select');

    $value.text(colorText);
    $value.append('<span style="background:' + color + '"></span>');
    $this.parents('ul').hide();
    $select.val(color);
  });

$(function () {
  $('[data-colorselect]').colorSelect();
});

// Show selected Classified Styles on the Review page

/*******************************************************
 *
 * Show selected Classified Styles on the Review page
 *
 */

// Store Style Name
$(document).ready(function () {
  // Add event listener for input field
  $('.styleName').on('input', function () {
    var styleName = $(this).val(); // Get the value entered by the user
    $('.style-name').text(styleName); // Update the content of the target HTML element
  });
});

$(document).ready(function () {
  // Add click event listener to color blocks
  $('.color-block').click(function () {
    $(this).toggleClass('selected');

    // Update the selected colors display
    updateSelectedColors();
  });
});

function updateSelectedColors() {
  // Get the selected colors container
  var selectedColorsContainer = $('#selectedColors .colors');

  // Clear existing content
  selectedColorsContainer.empty();

  // Loop through color blocks
  $('.color-block.selected').each(function () {
    var colorBlock = $(this).clone();
    colorBlock.find('.check').remove(); // Remove the span with the check icon
    selectedColorsContainer.append(colorBlock);
  });
}

document.addEventListener('DOMContentLoaded', function () {
  // Set the initial state of the selected color option
  var selectedColorOption = document.getElementById('selectedColorOption');
  selectedColorOption.textContent = 'Spot Color';
});

// Map option values to display names
const optionDisplayNames = {
  'spot-color': 'Spot Color',
  'black-white': 'Black & White',
  grayscale: 'Grayscale'
};

// Add event listener to the select element
document.getElementById('fontColorSelect').addEventListener('change', function () {
  // Get the selected color option value
  var selectedOptionValue = this.value;

  // Get the corresponding display name from the map
  var selectedOptionDisplayName = optionDisplayNames[selectedOptionValue];

  // Update the content of the selected color options div
  var selectedColorOption = document.getElementById('selectedColorOption');
  selectedColorOption.textContent = selectedOptionDisplayName;
});

// Add selected Pubs to review page

$(document).ready(function () {
  // Add click event listener to the "Move to Right" button
  $('#btnRight').click(function () {
    // Move selected publications from lstBox1 to lstBox2
    $('#lstBox1 option:selected').appendTo('#lstBox2');
    // Update the content of the target HTML element
    updateSelectedPublications();
  });

  // Add click event listener to the "Move to Left" button
  $('#btnLeft').click(function () {
    // Move selected publications from lstBox2 to lstBox1
    $('#lstBox2 option:selected').appendTo('#lstBox1');
    // Update the content of the target HTML element
    updateSelectedPublications();
  });
});

function updateSelectedPublications() {
  // Get the selected publications container
  var selectedPubsContainer = $('#selectedPubs select');

  // Clear existing content
  selectedPubsContainer.empty();

  // Loop through the options in lstBox2 and append them to the container
  $('#lstBox2 option').each(function () {
    selectedPubsContainer.append($(this).clone());
  });
}

// Show Avaiable in Self Service

$(document).ready(function () {
  // Set the initial value of selfService div based on the default checked radio button
  $('#selfServiceValue').text($('input[name="self-service-switch-option"]:checked').val());

  // Add change event listener to the radio buttons
  $('.radio-toggle').change(function () {
    // Get the value of the selected radio button
    var selectedValue = $('input[name="self-service-switch-option"]:checked').val();

    // Update the content of the target HTML element
    $('#selfServiceValue').text(selectedValue);
  });
});

/**
 * Upsells
 */

document.addEventListener('DOMContentLoaded', function () {
  // Find all custom-switch containers
  const switchContainers = document.querySelectorAll('.upsell-switch-container');

  // Loop through each custom-switch container
  switchContainers.forEach(container => {
    // Find all radio buttons within the container
    const radioButtons = container.querySelectorAll('input[type="radio"]');

    // Find the effects container for this switch
    const effectsContainer = container.closest('.upsell-item');

    // Add change event listener to each radio button
    radioButtons.forEach(radioButton => {
      radioButton.addEventListener('change', function () {
        // Check if the "no" option is checked
        const noOptionChecked = container.querySelector('input[type="radio"][value="inactive"]:checked');

        // Toggle the disabled class based on the "no" option
        if (effectsContainer) {
          if (noOptionChecked) {
            effectsContainer.classList.add('inactive');
          } else {
            effectsContainer.classList.remove('inactive');
          }
        } else {
          console.error('Effects container not found.');
        }
      });
    });
  });
});
