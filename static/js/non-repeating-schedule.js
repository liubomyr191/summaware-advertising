document.addEventListener('DOMContentLoaded', function () {
  const repeatRadio = document.getElementById('calendar-radio-one');
  const nonRepeatRadio = document.getElementById('calendar-radio-two');
  const repeatingCalendar = document.querySelector('.repeating-calendar');
  const nonRepeatingCalendar = document.querySelector('.non-repeating');
  const repeatDeadlines = document.querySelector('.repeat-deadlines-container');
  const productDeadlines = document.querySelector('.product-deadlines-container');

  // console.log(repeatRadio, nonRepeatRadio, repeatingCalendar, nonRepeatingCalendar, repeatDeadlines, productDeadlines);

  if (repeatRadio && nonRepeatRadio && repeatingCalendar && nonRepeatingCalendar && repeatDeadlines && productDeadlines) {
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
  } else {
    console.error('One or more required elements not found.');
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const scheduleBtn = document.querySelector('.start-schedule-button');
  const scheduleParent = document.querySelector('.non-repeating-parent');

  function addDeleteFunctionality(button) {
    button.addEventListener('click', function () {
      this.closest('.col-md-12.col-lg-6').remove();
    });
  }

  scheduleBtn.addEventListener('click', function () {
    const newScheduleBlock = `
                <div class="col-md-12 col-lg-6">
                  <div class="non-repeating-container">
                    <button class="delete-schedule-btn">
                      <i class="fa fa-solid fa-trash"></i>
                    </button>
                    <div class="row">
                      <div class="col-md-12 col-lg-6">
                        <div class="form-group">
                          <label for="">Name:</label>
                          <input type="text" name="product_name" id="" class="form-control" />
                        </div>
                      </div>
                      <div class="col-md-12 col-lg-6">
                        <label for="">Product Type:</label>
                        <select name="product_type" id="" class="form-control">
                          <option value="magazine">Magazine</option>
                          <option value="newspaper">Newspaper</option>
                          <option value="digital">Digital</option>
                        </select>
                      </div>
                    </div>

                    <div class="row">
                      <div class="col-md-12 col-lg-6">
                        <div>
                          <label for="gl-override">GL Override (optional)</label>
                        </div>
                        <div class="toggle-switch-container">
                          <div class="switch-field">
                            <input type="radio" id="non-repeat-gl-override-radio-one" name="gl_override" value="Yes" checked />
                            <label for="non-repeat-gl-override-radio-one">Yes</label>
                            <input type="radio" id="non-repeat-gl-override-radio-two" name="gl_override" value="No" />
                            <label for="non-repeat-gl-override-radio-two">No</label>
                          </div>
                        </div>
                      </div>
                      <div class="col-md-12 col-lg-6">
                        <label for="">GL Code:</label>
                        <select name="gl_code" id="" class="form-control">
                          {% for gl_code in gl_codes %}
                          <option value="{{gl_code.id}}">{{gl_code.code}}</option>
                          {% endfor %}
                        </select>
                      </div>
                    </div>

                    <div class="row mgt-1">
                      <div class="col-md-12 col-lg-4">
                        <div class="form-group">
                          <label for="">Publish Date:</label>
                          <input type="date" name="start_date" id="" class="form-control" />
                        </div>
                      </div>
                      <div class="col-md-12 col-lg-8">
                        <div class="content-even">
                          <div class="form-group w50 mgr-1">
                            <label for="">Publish Deadline:</label>
                            <input type="date" name="end_date" id="" class="form-control" />
                          </div>
                          <div class="w50 content-even mgt-1">
                            <div class="w50"><input type="text" name="" id="" class="form-control"></div>
                            <div class="px-05">at</div>
                            <div class="w50">
                              <select name="" id="" class="form-control">
                                <option>AM</option>
                                <option>PM</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="content-end mgb-1">
                      <button class="btn btn-link">
                        <strong>+ Add Date &amp; Deadline</strong>
                      </button>
                    </div>
                    <div class="chosen-dates">
                      <span>Chosen Days &amp; Deadlines</span>
                      <div class="table-container mt-3">
                        <table class="table">
                          <thead>
                            <tr>
                              <th scope="col">Publish Date</th>
                              <th scope="col">Publish Deadline</th>
                              <th scope="col"></th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr class="inactive">
                              <td>03/05/2024</td>
                              <td>03/05/2024 at 12:00PM</td>
                              <td>
                                <i class="fa fa-solid fa-trash"></i></span>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>`;
    scheduleParent.insertAdjacentHTML('beforeend', newScheduleBlock);

    const newDeleteButton = scheduleParent.querySelector('.col-md-12.col-lg-6:last-child .delete-schedule-btn');
    addDeleteFunctionality(newDeleteButton);
  });

  document.querySelectorAll('.delete-schedule-btn').forEach(button => {
    addDeleteFunctionality(button);
  });
});

// document.addEventListener('DOMContentLoaded', function () {
//   const scheduleBtn = document.querySelector('.start-schedule-button');
//   const scheduleParent = document.querySelector('.non-repeating-parent');

//   if (!scheduleParent) {
//     console.error('Parent element with class "non-repeating-parent" not found.');
//     return;
//   }

//   function addDeleteFunctionality(button) {
//     button.addEventListener('click', function () {
//       this.closest('.col-md-12.col-lg-6').remove();
//     });
//   }

//   scheduleBtn.addEventListener('click', function () {
//     const newScheduleBlock = `
//                 <div class="col-md-12 col-lg-6">
//                   <div class="non-repeating-container">
//                     <!-- your HTML content -->
//                   </div>
//                 </div>`;
//     scheduleParent.insertAdjacentHTML('beforeend', newScheduleBlock);

//     const newDeleteButton = scheduleParent.querySelector('.col-md-12.col-lg-6:last-child .delete-schedule-btn');
//     addDeleteFunctionality(newDeleteButton);
//   });

//   document.querySelectorAll('.delete-schedule-btn').forEach(button => {
//     addDeleteFunctionality(button);
//   });
// });
