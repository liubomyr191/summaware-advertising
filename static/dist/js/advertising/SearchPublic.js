const searchpubInput = document.querySelector('#search-pub');

const publicationelement = document.querySelector('.publication');

searchpubInput.addEventListener('keyup', () => {
    const searchValue = searchpubInput.value;

    searchPublicationElement(searchValue);
});

const searchPublicationElement = (searchValue) => {
    // Convert HTMLCollection to an array
    var elementsArray = Array.from(publicationelement.children);

    elementsArray.forEach(row => {
      const rowTitle = row.querySelector('.pub_name').innerText;

      if (searchValue === "") {
          row.style.display = '';
      } else if (!rowTitle.toLowerCase().includes(searchValue.toLowerCase())) {
          row.style.display = 'none';
      }
    })
}