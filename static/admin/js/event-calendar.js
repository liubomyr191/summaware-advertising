 var today = moment();
  var selectedDates = [];
  const tooltip = document.createElement('div');
  tooltip.className = 'td-tooltip';
  document.body.appendChild(tooltip);

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
  document.getElementById("calendar").innerHTML = perpetualCalendar;

  document.getElementById('prev-month-btn').addEventListener('click', showPreviousMonth);
  document.getElementById('next-month-btn').addEventListener('click', showNextMonth);
  document.getElementById('month-selector').addEventListener('change', showSelectedMonth);
  document.getElementById('year-selector').addEventListener('change', showSelectedYear);

  // Function to populate month and year selectors
  function populateSelectors() {
    const monthSelector = document.getElementById('month-selector');
    const yearSelector = document.getElementById('year-selector');
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
    const monthSelector = document.getElementById('month-selector');
    const currentMonth = parseInt(monthSelector.value, 10);
    const newMonth = currentMonth === 1 ? 12 : currentMonth - 1;
    const newYear = currentMonth === 1 ? parseInt(document.getElementById('year-selector').value, 10) - 1 : parseInt(document.getElementById('year-selector').value, 10);
    monthSelector.value = newMonth;
    document.getElementById('year-selector').value = newYear;
    // Update your calendar with the new month and year
    const perpetualCalendar = getPerpetualCalendar(newYear, newMonth);
    document.getElementById("calendar").innerHTML = perpetualCalendar;
  }

  // Function to show the next month
  function showNextMonth() {
    const monthSelector = document.getElementById('month-selector');
    const currentMonth = parseInt(monthSelector.value, 10);
    const newMonth = currentMonth === 12 ? 1 : currentMonth + 1;
    const newYear = currentMonth === 12 ? parseInt(document.getElementById('year-selector').value, 10) + 1 : parseInt(document.getElementById('year-selector').value, 10);
    monthSelector.value = newMonth;
    document.getElementById('year-selector').value = newYear;
    // Update your calendar with the new month and year
    const perpetualCalendar = getPerpetualCalendar(newYear, newMonth);
    document.getElementById("calendar").innerHTML = perpetualCalendar;
  }

  // Function to show the selected month
  function showSelectedMonth() {
    const selectedMonth = parseInt(document.getElementById('month-selector').value, 10);
    const selectedYear = parseInt(document.getElementById('year-selector').value, 10);
    // Update your calendar with the selected month and year
    const perpetualCalendar = getPerpetualCalendar(selectedYear, selectedMonth);
    document.getElementById("calendar").innerHTML = perpetualCalendar;
  }

  // Function to show the selected year
  function showSelectedYear() {
    const selectedYear = parseInt(document.getElementById('year-selector').value, 10);
    const selectedMonth = parseInt(document.getElementById('month-selector').value, 10);
    // Update your calendar with the selected month and year
    const perpetualCalendar = getPerpetualCalendar(selectedYear, selectedMonth);
    document.getElementById("calendar").innerHTML = perpetualCalendar;
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
    document.getElementById("calendar").innerHTML = perpetualCalendar;
  }

  function getTooltipText(year, month, day) {
    const selectedDate = selectedDates.find(date => date.year === year && date.month === month && date.day === day);

    if (selectedDate) {
      const numAdsBooked = selectedDate.adsBooked || 0;
      return numAdsBooked + ' ad' + (numAdsBooked !== 1 ? 's' : '') + ' have been booked';
    }

    return '';
  }

  function showTooltip(element, text) {
    // Set tooltip text
    tooltip.textContent = text;

    // Create a slider container
    const sliderContainer = document.createElement('div');
    sliderContainer.className = 'slider-container';

    // Create a slider fill
    const sliderFill = document.createElement('div');
    sliderFill.className = 'slider-fill';

    // Append the slider fill to the slider container
    sliderContainer.appendChild(sliderFill);

    // Append the slider container to the tooltip
    tooltip.appendChild(sliderContainer);

    // Append the tooltip to the document body
    document.body.appendChild(tooltip);

    // Position tooltip using CSS
    const modal = document.getElementById('create-ad');
    const topPosition = window.scrollY + modal.getBoundingClientRect().top + element.getBoundingClientRect().bottom;
    const leftPosition = modal.getBoundingClientRect().left + element.getBoundingClientRect().left;

    tooltip.style.position = 'absolute';
    tooltip.style.top = (topPosition + 10) + 'px';
    tooltip.style.left = (leftPosition - 75) + 'px';
    tooltip.style.display = 'block';
    tooltip.style.zIndex = '9999';
    tooltip.style.backgroundColor = 'white';
    tooltip.style.color = 'black';
    tooltip.style.padding = '5px';
    tooltip.style.borderRadius = '3px';
    tooltip.style.fontSize = '12px';
    tooltip.style.border = '1px solid black';
    tooltip.style.borderRadius = '3px';

  }


  function hideTooltip() {
    // Hide the tooltip
    tooltip.style.display = 'none';
  }

  document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('calendar').addEventListener('click', function(event) {
      if (event.target.tagName === 'TD') {
        const dayValue = parseInt(event.target.textContent, 10);
        selectDate(parseInt(document.getElementById('year-selector').value, 10), parseInt(document.getElementById('month-selector').value, 10), dayValue);
      }
    });
  });
  document.getElementById('calendar').addEventListener('mouseover', function (event) {
    if (event.target.tagName === 'TD') {
      const dayValue = parseInt(event.target.textContent, 10);
      // const tooltipText = `5 ads have been booked`;
      const tooltipText = `5 ads have been booked for ${dayValue}/${parseInt(document.getElementById('month-selector').value, 10)}/${parseInt(document.getElementById('year-selector').value, 10)}`;
      showTooltip(event.target, tooltipText);
    }
  });

  document.getElementById('calendar').addEventListener('mouseout', function (event) {
    if (event.target.tagName === 'TD') {
      hideTooltip();
    }
  });

  // Call the function to populate selectors initially
  populateSelectors();
