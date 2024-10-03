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
