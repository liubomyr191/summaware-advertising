$(document).ready(function() {
	$('#qbColumns td').contextmenu(function(e) {
		e.preventDefault()
		console.log(parserData);
		$('#exampleModalLong').modal('show');
	});
});