const searchInput = document.querySelector('#ad-search-input');

const campaignTable = document.querySelector('#campaign-table');
const campaignTableBody = campaignTable.querySelector('#campaign-table-tb');
const campaignTableRows = campaignTableBody.querySelectorAll('#campaign-table-row');

searchInput.addEventListener('keyup', () => {
    const searchValue = searchInput.value;
    searchCampaign(searchValue)
});

const searchCampaign = (searchValue) => {
    campaignTableRows.forEach(row => {
        const rowTitle = row.querySelector('#td:nth-child(2)').innerText;
        const rowCreator = row.querySelector('#td:nth-child(6)').innerText;
        const rowFormat = row.querySelector('#td:nth-child(8)').innerText;
        const rowAmount = row.querySelector('#td:nth-child(7)').innerText;

        if (searchValue === "") {
            row.style.display = '';
        } else if (!rowTitle.toLowerCase().includes(searchValue.toLowerCase()) && !rowCreator.toLowerCase().includes(searchValue.toLowerCase()) && !rowFormat.toLowerCase().includes(searchValue.toLowerCase()) && !rowAmount.toLowerCase().includes(searchValue.toLowerCase()))
            row.style.display = 'none';
    });
}