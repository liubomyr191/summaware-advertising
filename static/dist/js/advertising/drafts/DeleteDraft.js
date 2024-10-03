console.log('DeleteDraft.js');
var deleteLinks = document.querySelectorAll('.delete-draft-link');

deleteLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        var draftId = this.getAttribute('data-draft-id');
        var accountId = this.getAttribute('data-account-id');

        console.log()

        if (window.location.href.indexOf('account') > -1) {
            console.log('account id found');
            var url = "/advertising/account/" + accountId + "/drafts/" + draftId + "/delete/";

            document.getElementById('deleteBtn').addEventListener('click', function() {
                window.location.href = url;
            });
        } else {
            console.log('account id not found');
            var url = "/advertising/drafts/" + draftId + "/delete/";

            document.getElementById('deleteBtn').addEventListener('click', function() {
                window.location.href = url;
            });
        }
    });
})