// Disable list item inputs in deadlines

document.addEventListener('DOMContentLoaded', function () {
  const listItems = document.querySelectorAll('.list-group-item');

  listItems.forEach(item => {
    const onRadio = item.querySelector('input[type="radio"][value="on"]');
    const offRadio = item.querySelector('input[type="radio"][value="off"]');
    const inputs = item.querySelectorAll('.form-control');

    function toggleInputs() {
      if (offRadio.checked) {
        inputs.forEach(input => (input.disabled = true));
      } else {
        inputs.forEach(input => (input.disabled = false));
      }
    }

    onRadio.addEventListener('change', toggleInputs);
    offRadio.addEventListener('change', toggleInputs);

    // Initial state
    toggleInputs();
  });
});

// DOW Selector

document.addEventListener('DOMContentLoaded', function () {
  const checkboxes = document.querySelectorAll('.dow-picker-option input[type="checkbox"]');
  const tabContent = document.querySelectorAll('.tab-content .tab-pane');
  const navPills = document.querySelectorAll('.nav-pills li');

  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      const day = this.getAttribute('data-day');
      const tabPane = document.querySelector(`#${day}`);
      const navItem = document.querySelector(`.nav-pills li a[href="#${day}"]`).parentElement;

      // Remove active class from all tab panes and nav items
      tabContent.forEach(pane => pane.classList.remove('in', 'active'));
      navPills.forEach(item => item.classList.remove('active'));

      if (this.checked) {
        tabPane.classList.add('in', 'active');
        navItem.classList.remove('disabled');
        navItem.classList.add('active');
      } else {
        tabPane.classList.remove('in', 'active');
        navItem.classList.add('disabled');
        navItem.classList.remove('active');
      }
    });
  });

  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      if (this.checked) {
        this.closest('.dow-picker-option').classList.add('checked');
      } else {
        this.closest('.dow-picker-option').classList.remove('checked');
      }
    });
  });
});

// document.addEventListener('DOMContentLoaded', function () {
//   const checkboxes = document.querySelectorAll('.dow-picker-option input[type="checkbox"]');
//   const scheduleButtonsContainer = document.querySelector('.deadline-schedule-btns');

//   function updateSelectedDays() {
//     // Clear existing buttons
//     scheduleButtonsContainer.innerHTML = '';

//     // Create and add buttons for each selected day
//     checkboxes.forEach(checkbox => {
//       if (checkbox.checked) {
//         const label = checkbox.nextElementSibling;
//         const button = document.createElement('button');
//         button.type = 'button';
//         button.className = 'schedule-select-btn deadlines-schedule-btn';
//         button.textContent = label.innerText;
//         scheduleButtonsContainer.appendChild(button);
//       }
//     });

//     // Add js-active class to the first button
//     const firstButton = scheduleButtonsContainer.querySelector('.schedule-select-btn');
//     if (firstButton) {
//       firstButton.classList.add('js-active');
//     }

//     // Reattach event listeners for the new buttons
//     attachButtonListeners();
//   }

//   function attachButtonListeners() {
//     const buttons = scheduleButtonsContainer.querySelectorAll('.deadlines-schedule-btn');
//     buttons.forEach(button => {
//       button.addEventListener('click', function () {
//         // Remove js-active class from all buttons
//         buttons.forEach(btn => btn.classList.remove('js-active'));
//         // Add js-active class to the clicked button
//         this.classList.add('js-active');
//       });
//     });
//   }

//   checkboxes.forEach(checkbox => {
//     checkbox.addEventListener('change', function () {
//       if (this.checked) {
//         this.closest('.dow-picker-option').classList.add('checked');
//       } else {
//         this.closest('.dow-picker-option').classList.remove('checked');
//       }
//       updateSelectedDays();
//     });
//   });

//   // Initial update in case some checkboxes are already checked
//   updateSelectedDays();
// });

// End DOW Selector

// Publication Scheduling Repeat / Non Repeat Toggle

document.addEventListener('DOMContentLoaded', function () {
  const repeatRadio = document.getElementById('calendar-radio-one');
  const nonRepeatRadio = document.getElementById('calendar-radio-two');
  const repeatingCalendar = document.querySelector('.repeating-calendar');
  const nonRepeatingCalendar = document.querySelector('.non-repeating');
  const repeatDeadlines = document.querySelector('.repeat-deadlines-container');
  const productDeadlines = document.querySelector('.product-deadlines-container');

  repeatRadio.addEventListener('change', function () {
    if (repeatRadio.checked) {
      repeatingCalendar.classList.add('active');
      repeatingCalendar.classList.remove('hide');
      nonRepeatingCalendar.classList.add('hide');
      nonRepeatingCalendar.classList.remove('active');
      repeatDeadlines.classList.add('active');
      repeatDeadlines.classList.remove('hide');
      productDeadlines.classList.add('hide');
      productDeadlines.classList.remove('active');
    }
  });

  nonRepeatRadio.addEventListener('change', function () {
    if (nonRepeatRadio.checked) {
      nonRepeatingCalendar.classList.add('active');
      nonRepeatingCalendar.classList.remove('hide');
      repeatingCalendar.classList.add('hide');
      repeatingCalendar.classList.remove('active');
      repeatDeadlines.classList.add('hide');
      repeatDeadlines.classList.remove('active');
      productDeadlines.classList.add('active');
      productDeadlines.classList.remove('hide');
    }
  });
});

// End Publication Scheduling Repeat / Non Repeat Toggle

// Publication Schedule Toggle

document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.scheduling-btn');

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      // Remove js-active class from all buttons
      buttons.forEach(btn => btn.classList.remove('js-active'));
      // Add js-active class to the clicked button
      this.classList.add('js-active');
    });
  });
});

// End Publication Schedule Toggle

// Publication Deadline Schedule Toggle

document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.deadlines-schedule-btn');

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      // Remove js-active class from all buttons
      buttons.forEach(btn => btn.classList.remove('js-active'));
      // Add js-active class to the clicked button
      this.classList.add('js-active');
    });
  });
});

// End Publication Deadline Schedule Toggle

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

$(document).ready(function () {
  $('#btnRight').click(function (e) {
    var selectedOpts = $('#lstBox1 option:selected');
    if (selectedOpts.length == 0) {
      alert('Nothing to move.');
      e.preventDefault();
    }

    $('#lstBox2').append($(selectedOpts).clone());
    $(selectedOpts).remove();
    e.preventDefault();
  });

  $('#btnLeft').click(function (e) {
    var selectedOpts = $('#lstBox2 option:selected');
    if (selectedOpts.length == 0) {
      alert('Nothing to move.');
      e.preventDefault();
    }

    $('#lstBox1').append($(selectedOpts).clone());
    $(selectedOpts).remove();
    e.preventDefault();
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

// GL Code String Builder
var buttonsInDiv2 = [];

// Function to create input fields
function createInputField(buttonId) {
  var colDiv = document.createElement('div');
  colDiv.className = 'col-2';

  var label = document.createElement('label');
  label.textContent = buttonId.replace('drag', '');
  label.setAttribute('for', buttonId);

  var input = document.createElement('input');
  input.type = 'text';
  input.className = 'form-control';
  input.name = buttonId.replace('drag', ''); // Use buttonId to name inputs
  input.id = buttonId.replace('drag', ''); // Use buttonId as input id

  // Determine initial disabled state based on the location of the button
  input.disabled = !buttonsInDiv2.includes(buttonId);

  colDiv.appendChild(label);
  colDiv.appendChild(input);

  return colDiv;
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData('text', ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData('text');
  var draggedElement = document.getElementById(data);
  var dropZone = ev.target;

  // Check if the dropped element is a button and if the dropZone is "div2"
  if (draggedElement.tagName === 'BUTTON' && dropZone.id === 'div2') {
    // Move the button to the drop zone
    dropZone.appendChild(draggedElement);

    // Update the buttonsInDiv2 array to reflect the new order of buttons
    buttonsInDiv2 = Array.from(dropZone.querySelectorAll('button')).map(function (button) {
      return button.id;
    });

    // Update input fields based on buttonsInDiv2 array
    var inputContainer = document.getElementById('inputContainer');
    inputContainer.innerHTML = ''; // Clear existing input fields
    buttonsInDiv2.forEach(function (buttonId) {
      inputContainer.appendChild(createInputField(buttonId));
    });

    // Enable the corresponding input field
    var input = document.getElementById(draggedElement.id.replace('drag', ''));
    if (input) {
      input.disabled = false;
    }
  }

  // Check if the dropZone is "div1"
  if (dropZone.id === 'div1') {
    // Move the button back to the drop zone
    dropZone.appendChild(draggedElement);

    // Disable the corresponding input field
    var input = document.getElementById(draggedElement.id.replace('drag', ''));
    if (input) {
      input.disabled = true;
    }
  }
}

// Observe changes in div2 to detect button removal
var div2Observer = new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    mutation.removedNodes.forEach(function (node) {
      if (node.tagName === 'BUTTON') {
        // Update the buttonsInDiv2 array to reflect the new order of buttons
        buttonsInDiv2 = Array.from(document.getElementById('div2').querySelectorAll('button')).map(function (button) {
          return button.id;
        });

        // Update input fields based on buttonsInDiv2 array
        var inputContainer = document.getElementById('inputContainer');
        inputContainer.innerHTML = ''; // Clear existing input fields
        buttonsInDiv2.forEach(function (buttonId) {
          inputContainer.appendChild(createInputField(buttonId));
        });
      }
    });
  });
});
var elementDiv2 = document.getElementById('div2');
if (elementDiv2) {
  // Start observing changes in div2
  div2Observer.observe(elementDiv2, { childList: true });
}

// Observe changes in div1 to detect button addition
var div1Observer = new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    mutation.addedNodes.forEach(function (node) {
      if (node.tagName === 'BUTTON') {
        // Disable the corresponding input field
        var input = document.getElementById(node.id.replace('drag', ''));
        if (input) {
          input.disabled = true;
        }
      }
    });
  });
});

var elementDiv1 = document.getElementById('div1');
if (elementDiv1) {
  // Start observing changes in div2
  div1Observer.observe(elementDiv2, { childList: true });
}
