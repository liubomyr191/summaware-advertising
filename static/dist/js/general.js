$(document).ready(function() {
	$('#settings-sidebar').click(function() {
		$('body').toggleClass('settings-sidebar-collapse');
	});
	$(document).on('click', '#search_button', function() {
		$('body').toggleClass('search');
	});
});