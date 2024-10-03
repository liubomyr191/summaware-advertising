// Font Selector
document.addEventListener('DOMContentLoaded', function () {
  const fonts = [
    { name: 'Andale Mono', options: 'andale mono,times' },
    { name: 'Arial', options: 'arial,helvetica,sans-serif' },
    { name: 'Arial Black', options: 'arial black,avant garde' },
    { name: 'Book Antiqua', options: 'book antiqua,palatino' },
    { name: 'Comic Sans MS', options: 'comic sans ms,sans-serif' },
    { name: 'Courier New', options: 'courier new,courier' },
    { name: 'Georgia', options: 'georgia,palatino' },
    { name: 'Helvetica', options: 'helvetica' },
    { name: 'Impact', options: 'impact,chicago' },
    { name: 'Oswald', options: 'oswald' },
    { name: 'Symbol', options: 'symbol' },
    { name: 'Tahoma', options: 'tahoma,arial,helvetica,sans-serif' },
    { name: 'Terminal', options: 'terminal,monaco' },
    { name: 'Times New Roman', options: 'times new roman,times' },
    { name: 'Trebuchet MS', options: 'trebuchet ms,geneva' },
    { name: 'Verdana', options: 'verdana,geneva' },
    { name: 'Webdings', options: 'webdings' },
    { name: 'Wingdings', options: 'wingdings,zapf dingbats' }
  ];

  const fontSelect = document.getElementById('fontSelect');
  const sampleText = document.getElementById('sampleText');
  const selectedFontsContainer = document.querySelector('.selected-fonts-container');
  const fontsList = document.querySelector('.fonts-list');
  const fontPreview = document.querySelector('.font-preview');

  // Populate font selector dropdown
  fonts.forEach(font => {
    const option = document.createElement('option');
    option.value = font.options;
    option.textContent = font.name;
    fontSelect.appendChild(option);
  });

  // Function to change font family
  function changeFont() {
    const selectedOptions = Array.from(fontSelect.selectedOptions).map(option => option.textContent);
    // sampleText.style.fontFamily = selectedOptions.join(',');
    fontPreview.style.fontFamily = selectedOptions.join(',');
    updateSelectedFonts(selectedOptions);
  }

  // Event listener for font change
  fontSelect.addEventListener('change', changeFont);

  // Function to update selected fonts container
  function updateSelectedFonts(selectedFonts) {
    selectedFontsContainer.innerHTML = '';
    fontsList.innerHTML = ''; // Clear existing fonts list
    selectedFonts.forEach(font => {
      const selectedFontElement = document.createElement('span');
      selectedFontElement.classList.add('selected-font');
      selectedFontElement.textContent = font;
      selectedFontsContainer.appendChild(selectedFontElement);

      // Add selected font to fonts list
      const fontContainer = document.createElement('div');
      fontContainer.classList.add('font-container');
      const fontName = document.createElement('span');
      fontName.classList.add('font');
      fontName.textContent = font;
      fontContainer.appendChild(fontName);
      fontsList.appendChild(fontContainer);

      // Attach click event listener to newly added font container
      fontContainer.addEventListener('click', function () {
        // Toggle "active" class for font container
        const isActive = this.classList.contains('active');
        fontsList.querySelectorAll('.font-container').forEach(container => {
          container.classList.remove('active');
        });
        if (!isActive) {
          this.classList.add('active');
          fontPreview.style.fontFamily = font;
        }
      });
    });
  }
});

$(document).ready(function () {
  $('#btnRight').click(function (e) {
    var selectedOpts = $('#lstBox1 option:selected');
    if (selectedOpts.length == 0) {
      e.preventDefault();
    }

    $('#lstBox2').append($(selectedOpts).clone());
    $(selectedOpts).remove();
    e.preventDefault();
  });

  $('#btnLeft').click(function (e) {
    var selectedOpts = $('#lstBox2 option:selected');
    if (selectedOpts.length == 0) {
      e.preventDefault();
    }

    $('#lstBox1').append($(selectedOpts).clone());
    $(selectedOpts).remove();
    e.preventDefault();
  });
});

function toggleSearchContainer() {
  var searchContainer = document.getElementById('search-container');
  if (searchContainer.style.display === 'none' || searchContainer.style.display === '') {
    searchContainer.style.display = 'block';
  } else {
    searchContainer.style.display = 'none';
  }
}

function toggleNewCodePanel() {
  var newCodePanel = document.getElementById('new-code-panel');
  if (newCodePanel.style.display === 'none' || newCodePanel.style.display === '') {
    newCodePanel.style.display = 'block';
  } else {
    newCodePanel.style.display = 'none';
  }
}

function closeCodePanel() {
  var newCodePanel = document.getElementById('new-code-panel');
  if (newCodePanel.style.display === 'block') {
    newCodePanel.style.display = 'none';
  } else {
    newCodePanel.style.display = 'none';
  }
}

// Slide Out Tab

this.$slideOut = $('#slideOut');

// Slideout show
this.$slideOut.find('.slideOutTab').on('click', function () {
  $('#slideOut').toggleClass('showSlideOut');
});

const DOMstrings = {
  stepsBtnClass: 'multisteps-form__progress-btn',
  stepsBtns: document.querySelectorAll(`.multisteps-form__progress-btn`),
  stepsBar: document.querySelector('.multisteps-form__progress'),
  stepsForm: document.querySelector('.multisteps-form__form'),
  stepsFormTextareas: document.querySelectorAll('.multisteps-form__textarea'),
  stepFormPanelClass: 'multisteps-form__panel',
  stepFormPanels: document.querySelectorAll('.multisteps-form__panel'),
  stepPrevBtnClass: 'js-btn-prev',
  stepNextBtnClass: 'js-btn-next'
};

//remove class from a set of items
const removeClasses = (elemSet, className) => {
  elemSet.forEach(elem => {
    elem.classList.remove(className);
  });
};

//return exact parent node of the element
const findParent = (elem, parentClass) => {
  let currentNode = elem;

  while (!currentNode.classList.contains(parentClass)) {
    currentNode = currentNode.parentNode;
  }

  return currentNode;
};

//get active button step number
const getActiveStep = elem => {
  return Array.from(DOMstrings.stepsBtns).indexOf(elem);
};

//set all steps before clicked (and clicked too) to active
const setActiveStep = activeStepNum => {
  const buttons = document.querySelectorAll('.multisteps-form__progress-btn');
  const activeButton = document.querySelector('.js-active');

  // Remove the 'js-active' class from the currently active button
  activeButton.classList.remove('js-active');

  // Add the 'js-active' class to the clicked button
  buttons[activeStepNum].classList.add('js-active');
};

// STEPS BAR CLICK FUNCTION
DOMstrings.stepsBtns.forEach((button, index) => {
  button.addEventListener('click', () => {
    setActiveStep(index);
  });
});

//get active panel
const getActivePanel = () => {
  let activePanel;

  DOMstrings.stepFormPanels.forEach(elem => {
    if (elem.classList.contains('js-active')) {
      activePanel = elem;
    }
  });

  return activePanel;
};

//open active panel (and close unactive panels)
const setActivePanel = activePanelNum => {
  //remove active class from all the panels
  removeClasses(DOMstrings.stepFormPanels, 'js-active');

  //show active panel
  DOMstrings.stepFormPanels.forEach((elem, index) => {
    if (index === activePanelNum) {
      elem.classList.add('js-active');

      setFormHeight(elem);
    }
  });
};

//set form height equal to current panel height
const formHeight = activePanel => {
  const activePanelHeight = activePanel.offsetHeight;

  DOMstrings.stepsForm.style.height = `${activePanelHeight}px`;
};

const setFormHeight = () => {
  const activePanel = getActivePanel();

  formHeight(activePanel);
};

//STEPS BAR CLICK FUNCTION
DOMstrings.stepsBar.addEventListener('click', e => {
  //check if click target is a step button
  const eventTarget = e.target;

  if (!eventTarget.classList.contains(`${DOMstrings.stepsBtnClass}`)) {
    return;
  }

  //get active button step number
  const activeStep = getActiveStep(eventTarget);

  //set all steps before clicked (and clicked too) to active
  setActiveStep(activeStep);

  //open active panel
  setActivePanel(activeStep);
});

//PREV/NEXT BTNS CLICK
DOMstrings.stepsForm.addEventListener('click', e => {
  const eventTarget = e.target;

  //check if we clicked on `PREV` or NEXT` buttons or arrow buttons
  if (!(eventTarget.classList.contains(`${DOMstrings.stepPrevBtnClass}`) || eventTarget.classList.contains(`${DOMstrings.stepNextBtnClass}`) || eventTarget.classList.contains('fa-chevron-left') || eventTarget.classList.contains('fa-chevron-right'))) {
    return;
  }

  //find active panel
  const activePanel = findParent(eventTarget, `${DOMstrings.stepFormPanelClass}`);

  let activePanelNum = Array.from(DOMstrings.stepFormPanels).indexOf(activePanel);

  //set active step and active panel onclick
  if (eventTarget.classList.contains(`${DOMstrings.stepPrevBtnClass}`) || eventTarget.classList.contains('fa-chevron-left')) {
    activePanelNum--;
  } else {
    activePanelNum++;
  }

  // Ensure activePanelNum stays within bounds
  activePanelNum = Math.max(0, Math.min(activePanelNum, DOMstrings.stepFormPanels.length - 1));

  setActiveStep(activePanelNum);
  setActivePanel(activePanelNum);
});

//SETTING PROPER FORM HEIGHT ONLOAD
window.addEventListener('load', setFormHeight, false);

//SETTING PROPER FORM HEIGHT ONRESIZE
window.addEventListener('resize', setFormHeight, false);

document.addEventListener('DOMContentLoaded', function () {
  const panels = document.querySelectorAll('.multisteps-form__panel');
  const arrowLeft = document.querySelector('.multistep-form__arrow .fa-chevron-left');
  const arrowRight = document.querySelector('.multistep-form__arrow .fa-chevron-right');

  // Event listener for left arrow button
  arrowLeft.addEventListener('click', function () {
    const currentPanel = document.querySelector('.multisteps-form__panel.js-active');
    const currentIndex = Array.from(panels).indexOf(currentPanel);
    const nextIndex = Math.max(currentIndex - 1, 0);
    panels[currentIndex].classList.remove('js-active');
    panels[nextIndex].classList.add('js-active');
  });

  // Event listener for right arrow button
  arrowRight.addEventListener('click', function () {
    const currentPanel = document.querySelector('.multisteps-form__panel.js-active');
    const currentIndex = Array.from(panels).indexOf(currentPanel);
    const nextIndex = Math.min(currentIndex + 1, panels.length - 1);
    panels[currentIndex].classList.remove('js-active');
    panels[nextIndex].classList.add('js-active');
  });
});

function openSection(evt, sectionName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName('tabcontent');
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = 'none';
  }
  tablinks = document.getElementsByClassName('tablinks');
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(' active', '');
  }
  document.getElementById(sectionName).style.display = 'block';
  evt.currentTarget.className += ' active';
}

// Multistep

function next_step(event) {
  // Prevent the default button action if needed
  event.preventDefault();

  // Get the button that triggered the function
  var button = event.target;

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

  // Find the next section
  var nextSection = currentSection.nextElementSibling;

  // If there is no next section, exit the function
  if (!nextSection || !nextSection.classList.contains('multistep-content')) return;

  // Remove the 'hide' class from the next section
  nextSection.classList.remove('hide');

  // Get all progress icons within the specified form
  var progressIcons = document.querySelectorAll('.progress-icons > .progress-dot-container > div');

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
}

// function next_step() {
//   // Get the current active section
//   var currentSection = document.querySelector('.multistep-content:not(.hide)');

//   // Find the next section
//   var nextSection = currentSection.nextElementSibling;

//   // If there is no next section, exit the function
//   if (!nextSection) return;

//   // Remove the 'hide' class from the next section
//   nextSection.classList.remove('hide');

//   // Get all progress icons
//   var progressIcons = document.querySelectorAll('.progress-icons > .progress-dot-container > div');

//   // Find the index of the current active progress icon
//   var currentIndex;
//   progressIcons.forEach(function (icon, index) {
//     if (icon.classList.contains('progress-active')) {
//       currentIndex = index;
//     }
//   });

//   // If the current index is valid and there is a next progress icon, add 'progress-active' class to it
//   if (currentIndex !== undefined && progressIcons[currentIndex + 1]) {
//     progressIcons[currentIndex + 1].classList.add('progress-active');
//   }

//   // Hide the current section
//   currentSection.classList.add('hide');
// }

// Event listener setup for buttons
document.querySelectorAll('.next-step-button').forEach(function (button) {
  button.addEventListener('click', next_step);
});

function previous_step() {
  // Get the current active section
  var currentSection = document.querySelector('.multistep-content:not(.hide)');

  // Find the previous section
  var previousSection = currentSection.previousElementSibling;

  // If there is no previous section, exit the function
  if (!previousSection) return;

  // Remove the 'hide' class from the previous section
  previousSection.classList.remove('hide');

  // Get all progress icons
  var progressIcons = document.querySelectorAll('.progress-icons > .progress-dot-container > div');

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

function create_product() {
  // Get the current active section
  var currentSection = document.querySelector('.multistep-content:not(.hide)');

  // Find the last section
  var lastSection = document.querySelector('.multistep-content:last-of-type');

  // If the current section is the last section, exit the function
  if (currentSection === lastSection) return;

  // Remove the 'hide' class from the last section
  lastSection.classList.remove('hide');

  // Get all progress icons
  var progressIcons = document.querySelectorAll('.progress-icons > div');

  // Add the 'progress-active' class to the last progress icon
  progressIcons[progressIcons.length - 1].classList.add('progress-active');

  // Hide the current section
  currentSection.classList.add('hide');
}

document.addEventListener('DOMContentLoaded', function () {
  // Find all custom-switch containers
  const switchContainers = document.querySelectorAll('.custom-switch-container');

  // Loop through each custom-switch container
  switchContainers.forEach(container => {
    // Find all radio buttons within the container
    const radioButtons = container.querySelectorAll('input[type="radio"]');

    // Find the effects container for this switch
    const effectsContainer = container.closest('.effects-container');

    // Add change event listener to each radio button
    radioButtons.forEach(radioButton => {
      radioButton.addEventListener('change', function () {
        // Check if the "no" option is checked
        const noOptionChecked = container.querySelector('input[type="radio"][value="no"]:checked');

        // Toggle the disabled class based on the "no" option
        if (effectsContainer) {
          if (noOptionChecked) {
            console.log('No option selected. Adding disabled class.');
            effectsContainer.classList.add('disabled');
          } else {
            console.log('Yes option selected. Removing disabled class.');
            effectsContainer.classList.remove('disabled');
          }
        } else {
          console.error('Effects container not found.');
        }
      });
    });
  });
});
