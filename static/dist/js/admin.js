$(document).ready(function() {
	jQuery(".main-table").clone(true).appendTo('#table-scroll').addClass('clone');   
	
	$('. tr').click(function() {
		
	});

	window.onclick = function(event) {
		if (!event.target.matches('.dropbtn')) {
			var dropdowns = document.getElementsByClassName("dropdown-content");
			var i;
			for (i = 0; i < dropdowns.length; i++) {
				var openDropdown = dropdowns[i];
				if (openDropdown.classList.contains('show')) {
					openDropdown.classList.remove('show');
				}
			}
		}
	}
});