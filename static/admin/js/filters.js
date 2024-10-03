document.addEventListener('DOMContentLoaded', function () {
  const filterLinks = document.querySelectorAll('.upsell-filters span');
  const radioButtons = document.querySelectorAll('input[type="radio"]');

  filterLinks.forEach(function (link) {
    link.addEventListener('click', function (event) {
      event.preventDefault();
      const filterClass = event.target.textContent.toLowerCase();

      // Remove 'active' class from all filter links
      filterLinks.forEach(function (filterLink) {
        filterLink.classList.remove('active');
      });

      // Add 'active' class to the clicked filter link
      link.classList.add('active');

      if (filterClass === 'all') {
        showAllUpsellItems();
      } else {
        filterUpsellItems(filterClass);
      }
    });
  });

  radioButtons.forEach(function (radioButton) {
    radioButton.addEventListener('change', function () {
      const item = radioButton.closest('.upsell-item');
      const value = radioButton.value;

      if (value === 'yes') {
        item.classList.remove('inactive');
        item.classList.add('active');
      } else {
        item.classList.remove('active', 'archived');
        item.classList.add('inactive');
      }
    });
  });

  function showAllUpsellItems() {
    const items = document.querySelectorAll('.upsell-item');
    items.forEach(function (item) {
      item.style.display = 'block';
    });
  }

  function filterUpsellItems(filterClass) {
    const items = document.querySelectorAll('.upsell-item');
    items.forEach(function (item) {
      if (item.classList.contains(filterClass)) {
        item.style.display = 'block';
      } else {
        item.style.display = 'none';
      }
    });
  }
});

// function filterTableRows(filterClass) {
//   const rows = document.querySelectorAll('.table-container tbody tr');

//   rows.forEach(function (row) {
//     const statusCell = row.querySelector('.status-cell');
//     const selfServiceCell = row.querySelector('.self-service-cell');

//     if (filterClass === 'inactive' && statusCell.textContent.trim() === 'Inactive') {
//       row.style.display = 'table-row';
//     } else if (filterClass === 'archived' && selfServiceCell.textContent.trim() === 'Off') {
//       row.style.display = 'table-row';
//     } else if (filterClass === 'active') {
//       row.style.display = 'table-row';
//     } else {
//       row.style.display = 'none';
//     }
//   });
// }
