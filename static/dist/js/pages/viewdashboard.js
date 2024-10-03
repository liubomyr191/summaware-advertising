var drilldown_options = {};
var drilldown_titles = {};

$(document).ready(function() {
	var selected_field = '';
	var selected_value = '';
	var chart_id = '';
	var dashboard_id = '';
	var breadcrumbs = '';

	var csrftoken = getCookie('csrftoken');
	
	$('body').on('click', 'a.drilldown_breadcrumb', function() {
		chart_id = $(this).closest('div[chart_id]').attr('chart_id');
		dashboard_id = $('#dashboard_id').attr('dashboard_id');
		$("div[chart_id=" + chart_id + "]").find(".table-wrap").html('<div class="loader"></div>');		
		asyncRequest(csrftoken, $("div[chart_id=" + chart_id + "]"), chart_id, dashboard_id, null, null, null, null, $(this).attr('value'), null);
		chart_id = '';
	});

	$(".data").each(function(index) {
		dashboard_id = $('#dashboard_id').attr('dashboard_id');
		asyncRequest(csrftoken, this, $(this).attr('chart_id'), dashboard_id, null, null, null, null, null, null);
	});

	$('filter_checkbox').click(function(){

	});

	/*
	$('').click(function() {
		sorting = {'sort_by': '', 'sorting': ''};
		dashboard_id = $('#dashboard_id').attr('dashboard_id');
		asyncRequest(csrftoken, this, $(this).attr('chart_id'), dashboard_id, null, null, null, null, null, sorting);
	});
	*/
	
	/*
		------------
	*/

	// Close drilldown on x-mark (close button) clicked
	$('#close').click(function(e) {
		if ($('.drilldown').is(':visible')) {
			hideDrilldown();
		}
	});

	$('body').on('contextmenu', 'tbody td, path, tbody .sticky_col', function(e) {
		e.preventDefault();
		if ($('.menu_container').is(":visible")) {
			$('.selected').removeClass('selected');    
			$('.menu_container').toggle();

			selected_field = '';
			selected_value = '';
			chart_id = '';
		} else {
			$('.drilldown').hide();
			$(this).addClass('selected');
			$('.menu').remove();

			var select_text = '<dl class="menu"><dt>Select</dt><dd>' + $(this).attr('field') + '=' + $(this).attr('value') + '</dd>';
			if ($(this).attr('caption') != undefined) {
				select_text += '<dt>Drill</dt><dd type="drilldown">Choose Another..</dd>';
			}

			$('.menu_container').append(select_text + "</dl>");
			chart_id = $(this).closest('div[chart_id]').attr('chart_id');
			selected_field = $(this).attr('field');
			selected_value = $(this).attr('value');
			selected_position = $(this).attr('position');

			var pos1 = $(this).offset();
			$('.menu_container').toggle();
			$('.menu_container').offset({top: pos1.top + $(this).height(), bottom: pos1.bottom, left:pos1.left});					
		}
		return false;
	});

	$('body').on('click', 'dd[type="drilldown"]', function() {
		var pos2 = $(this).offset();
		$('.selected').removeClass('selected');
		$('.menu_container').toggle();
		if ($('.drilldown').is(":hidden") && $(this).attr("type") == "drilldown") {
			$('#drilldown_title').text(drilldown_titles[chart_id]);
			var temp = '';
			$.each(drilldown_options[chart_id], function(drilldown_table, drilldown_fields) {
				temp += '<dt>' + drilldown_table + '</dt>';
				$.each(drilldown_fields, function(drilldown_key, drilldown_field) {
					temp += '<dd class="drilldown_field" drilldown_id="' + drilldown_key + '">' + drilldown_field + '</dd>';
				});
			});
			$('#drilldown_dl').html(temp);
			$('.drilldown').toggle();
			$('.drilldown').offset({top: pos2.top, bottom: pos2.bottom, left:pos2.left});		
		}
	});

	$('body').on('change', '.filter_toggle', function() {
		dashboard_id = $('#dashboard_id').attr('dashboard_id');
		data = {'csrfmiddlewaretoken': csrftoken, 'dashboard_id': dashboard_id, 'filter_key': $(this).attr('filter_key'), 'filter_status': ''}
		if ($(this).is(':checked')) {
			$(this).closest('div').parent().parent().find('input, textarea, button, select').not('.filter_toggle').removeAttr('disabled');
			data.filter_status = 'on';
		} else {
			$(this).closest('div').parent().parent().find('input, textarea, button, select').not('.filter_toggle').attr('disabled', 'disabled');
			data.filter_status = 'off';
		}
		$.ajax({
			url: "/bi/ajax/toggle_filter?_=" + new Date().getTime(),
			type: "POST",
			data: data,
			complete: function (result) {
				let response = JSON.parse(result["responseText"]);
				if (response['message'] == 'success') {
					//location.reload();
					if ($('#reload_on_toggle')[0].checked) {
						window.location.assign(response['url']);
					}
				}
			},
			error: function (result) {
			}
		});
	});

	$('div.drilldown').on('click', 'dd', function(e) {
		$("div[chart_id=" + chart_id + "]").find(".table-wrap").html('<div class="loader"></div>');
		dashboard_id = $('#dashboard_id').attr('dashboard_id');
		asyncRequest(csrftoken, $("div[chart_id=" + chart_id + "]"), chart_id, dashboard_id, $(e.target).attr('drilldown_id'), selected_field, selected_value, selected_position, null, null);
		hideDrilldown();
		selected_field = '';
		selected_value = '';
		selected_position = '';
	});

	$(document).click(function(e){
		if (e.target.nodeName != 'DD' && $(e.target).parents('.drilldown').length == 0) {
			hideDrilldown();
			selected_field = '';
			selected_value = '';
		}

		if ($(e.target).hasClass('reset_dashboard')) {
			dashboard_id = $('#dashboard_id').attr('dashboard_id');
			$.ajax({
				url: "/bi/ajax/reset?_=" + new Date().getTime() + '&reset_id=' + dashboard_id + '&reset_type=dashboard',
				type: "GET",
				complete: function (result) {
					let response = JSON.parse(result["responseText"]);
					if (response['message'] == 'success') {
						location.reload();
					}
				},
				error: function (result) {
				}
			});
		} else if ($(e.target).hasClass('reset_chart')) { 
			chart_id = $(e.target).attr('chart_id');
			dashboard_id = $('#dashboard_id').attr('dashboard_id');
			$("div[chart_id=" + chart_id + "]").find(".table-wrap").html('<div class="loader"></div>');
			$.ajax({
				url: "/bi/ajax/reset?_=" + new Date().getTime() + '&reset_id=' + chart_id + '&reset_type=chart',
				type: "GET",
				complete: function (result) {
					let response = JSON.parse(result["responseText"]);
					if (response['message'] == 'success') {
						//location.reload();
						asyncRequest(csrftoken, $("div[chart_id=" + chart_id + "]"), chart_id, dashboard_id, null, null, null, null, null, null);
					}
				},
				error: function (result) {
				}
			});
		}
		/*
		} else if ($(e.target).hasClass('sortable')) {
			chart_id = $(e.target).closest('div[chart_id]').attr('chart_id');
			dashboard_id = $('#dashboard_id').attr('dashboard_id');
			let sort = $(e.target).attr('sort');
			let order = $(e.target).attr('order');

			if (order.toLowerCase() == 'asc') {
				order = 'desc';
			} else {
				order = 'asc';
			}
			$("div[chart_id=" + chart_id + "]").find(".table-wrap").html('<div class="loader"></div>');
			$.ajax({
				url: "/bi/ajax/resort?_=" + new Date().getTime() + '&dashboard_id=' + dashboard_id + '&chart_id=' + chart_id + '&sort=' + sort + '&order=' + order,
				type: "GET",
				complete: function (result) {
					let response = JSON.parse(result["responseText"]);
					if (response['message'] == 'success') {
						//location.reload();
						asyncRequest(csrftoken, $("div[chart_id=" + chart_id + "]"), chart_id, dashboard_id, null, null, null, null, null, null);
					} else {
						alert(response['message']);
					}
				},
				error: function (result) {
				}
			});
		}
		*/
	});

	/*
		------------
	*/
});

function getTableData(tableElem) {
	var data = [];
	for (var i = 1, l = tableElem.length-1; i < l; i++) {
		for (var j = 0, m = tableElem[i].cells.length; j < m; j++) {
			if (typeof data[i] === "undefined") {
				data[i] = {};
				data[i]["key"] = i;
			}
			data[i][j] = tableElem[i].cells[j].innerText;
		}
	}
	return data;
}

function sortEvent(elem) {
	var ascClass = "order-asc";
	var descClass = "order-desc";
	var closest = function(th) {
		var parent = th.parentNode;
		if (parent.tagName.toUpperCase() === "TABLE") {
			return parent;
		}
		return closest(parent);
	};
	var table = closest(elem);
	if (!table) {
		return;
	}

	var colNo = elem.cellIndex;
	var tableData = getTableData(table.querySelectorAll("tr"));

	var sortOrder = !elem.classList.contains(ascClass) ? 1 : -1;
	tableData.sort(function(a, b) {
		let a2 = strip(a[colNo]);
		let b2 = strip(b[colNo]);
		
		if (isNumber(a2) && isNumber(b2)) {
			if (sortOrder == -1) {
				return a2 - b2;
			} else {
				return b2 - a2;
			}
		} else {
			if (a2 < b2) {
				return -1 * sortOrder;
			} else if (a2 > b2) {
				return sortOrder;
			}
		}
		return 0;
	});

	var html = "";
	tableData.forEach(function(x) {
		html += table.querySelectorAll("tr")[x["key"]].outerHTML;
	});
	table.querySelector("tbody").innerHTML = html;

	var tableElem = table.querySelectorAll("thead th");
	Object.keys(tableElem).forEach(function(key) {
		tableElem[key].classList.remove(descClass);
		tableElem[key].classList.remove(ascClass);
	});
	if (sortOrder === 1) {
		elem.classList.add(ascClass);
	}else {
		elem.classList.add(descClass);
	}
}

function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }

function strip(value) {
	return value.replace('$', '').replace('%', '').replace(',', '');
}

function search() {
	var inputValue = $('#drilldown_search_input').val().toUpperCase();
	var textValue;
	$('.drilldown_field').each(function(key, value) {
		textValue = $(this).text().toUpperCase();
		if (textValue.indexOf(inputValue) > -1) {
			$(this).show();
		} else {
			$(this).hide();
		}
	});
}

function hideDrilldown() {
	$('#drilldown_search').find('input:text').val('');
	$('.selected').removeClass('selected');
	$('.menu_container').hide();
	$('.drilldown').hide();

	$('.drilldown_field').each(function(key, value) {
		$(this).show();
	});
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function asyncRequest(csrftoken, current, chart_id, dashboard_id, new_field_id, old_field, old_field_value, select_position, drilldown_breadcrumb, sorting) {
	var results = "";
	var data = {'csrfmiddlewaretoken': csrftoken, 'chart_id': chart_id, 'dashboard_id': dashboard_id};

	if (new_field_id != null && old_field != null && old_field_value != null && select_position != null) {
		data.new_field_id = new_field_id;
		data.old_field = old_field;
		data.old_field_value = old_field_value;
		data.select_position = select_position;
	}

	if (drilldown_breadcrumb != null) {
		data.drilldown_breadcrumb = drilldown_breadcrumb;
	}

	$.ajax({
		url: "/bi/ajax/?_=" + new Date().getTime(),
		type: "POST",
		data: data,
		complete: function (result) {
			displayResults(current, JSON.parse(result["responseText"]));
		},
		error: function (result) {
			displayResults(current, JSON.parse(result["responseText"]));
		}
	});
	return results;
}

function displayResults(current, results) {
	$(current).find(".loader").hide();
	if (results["message"] != "false") {
		var message = '';
		$(current).find(".box-title").html("Error");
		if (results['drilldown_breadcrumb'] != undefined && results['drilldown_breadcrumb'] != '') {
			message += results['drilldown_breadcrumb'];
		}
		message += results["message"];
		$(current).find(".table-wrap").html(message);
	} else {
		$(current).find(".box-title").html(results["title"]);
		displayChart(current, results);
	}
	drilldown_titles[results['chart_id']] = results['title'];
	drilldown_options[results['chart_id']] = results['drilldowns'];
}

function displayChart(current, results) {
	var chart = "";

	switch(results["chart_type"]) {
		case "table":
			$(current).find(".table-wrap").html(table(results));
			break;
		case "pie":
			$(current).find(".table-wrap").html('<div id="pieChart"></div>');
			pie(results);
			break;
	}
}

function table(results) {
	var dashboard_id = $('#dashboard_id').attr('dashboard_id');
	var attributes = JSON.parse(results["attributes"]);
	var colors = attributes.color.split(",");
	var sum = {'sum_ids': '', 'caption_ids': '','var_percent_ids': '', 'calc_var_percent_ids': ''};
	if (attributes.sum.ids != undefined)
		sum.sum_ids = attributes.sum.ids.split(",");

	if (attributes.sum.caption_ids != undefined)
		sum.caption_ids = attributes.sum.caption_ids.split(",");
	if (attributes.sum.var_percent_ids != undefined)
		sum.var_percent_ids = attributes.sum.var_percent_ids.split(',');
	if (attributes.sum.calc_var_percent_ids != undefined)
		sum.calc_var_percent_ids = attributes.sum.calc_var_percent_ids.split(',');

	var captioned = false;
	var total = {};
	var types = {};

	var table = ''
	if (results['drilldown_breadcrumb'] != undefined && results['drilldown_breadcrumb'] != '') {
		table += results['drilldown_breadcrumb'];
	}
	table += '<table id="example1" class="table table-bordered table-striped dataTable main-table" role="grid" aria-describedby="example1_info">\
					<thead>\
						<tr role="row">';

	for (var headers_index = 0; headers_index < results["headers"].length; headers_index++) {
		var sort = results["headers"][headers_index][0];
		var order = '';
		
		if (results["headers"][headers_index][0].toLowerCase() == results['sort'].toLowerCase()) {
			order = results['order'];
			sort = results["headers"][headers_index][0];
		}
		
		if (headers_index == 0) {
			table += '			<th class="' + (order != '' ? 'order-' + order : '') + ' sortable sticky_col' + (headers_index == 0 ? ' fixed-side' : ' col') + '" onclick="sortEvent(event.target)">' + sort + '</th>';
		} else {
			if (sum.caption_ids.indexOf(headers_index.toString()) > -1) {
				table += '			<th class="' + (order != '' ? 'order-' + order : '') + ' sortable' + (headers_index == 0 ? ' fixed-side' : ' col') + '" onclick="sortEvent(event.target)">' + sort + '</th>';
			} else {
				table += '			<th class="' + (order != '' ? 'order-' + order : '') + ' sortable' + (headers_index == 0 ? ' fixed-side' : ' col') + '" onclick="sortEvent(event.target)">' + sort + '</th>';
			}
		}
	}
	
	table +='			</tr>\
					</thead>\
				<tbody>';

	for (var index = 0; index < results["data"].length; index++) {
		var caption_field = '';
		var caption_value = '';
		table += '<tr role="row" class="' + (index % 2 ? 'odd' : 'even') + (index == 0 ? ' fixed-side' : '') + '">';
		for (var c = 0; c < results["data"][index].length; c++) {
			if (typeof total[c] == 'undefined') {
				types[c] = "";
				total[c] = 0;
			}

			let sticky = '';
			if (c == 0) {
				sticky = 'class="sticky_col" ';
			}

			if (colors.indexOf(c.toString()) > -1 && results["data"][index][c] != null) {
				table +='<td ' + sticky + 'field="' + caption_field + '" value="' + caption_value + '" position="' + c + '" style="background-color:' + (parseInt(results["data"][index][c].replaceAll(",","").replaceAll("%","").replaceAll("$","")) < 0 ? 'rgb(252, 117, 112)' : 'rgb(110, 218, 85)') + ';">' + results["data"][index][c] + '</td>';
			} else {
				if (sum.caption_ids.indexOf(c.toString()) > -1) {
					caption_field = results["headers"][c][0];
					caption_value = results["data"][index][c];

					table +='<td ' + sticky + 'style="" caption field="' + results["headers"][c][0] + '" value="' + results["data"][index][c] + '" position="' + c + '">' + results["data"][index][c] + '</td>';
				} else {

					table +='<td ' + sticky + 'style="" field="' + caption_field + '" value="' + caption_value + '" position="' + c + '">' + results["data"][index][c] + '</td>';
				}
			}

			if (sum.sum_ids.indexOf(c.toString()) > -1 && results["data"][index][c] != null) {

				if (results["data"][index][c].indexOf("$") !== -1) {
					types[c] = "$";
				}
				if (results["data"][index][c].indexOf("%") !== -1) {
					types[c] = "%";
				}

				var cell = results["data"][index][c].replaceAll(",","").replaceAll("%","").replaceAll("$","");
				if (!isNaN(cell)) {
					total[c] += parseFloat(cell);
				}
			}
		}
		table += '</tr>';

		if (index == (results["data"].length - 1) && sum.sum_ids.length > 0) {
			table += '</tbody><tfoot><tr>';
			for (var d = 0; d < results["data"][index].length; d++) {
				table += '<td>';
				if (types[d] == "$"){
					table += "$";
				}

				if (sum.caption_ids.indexOf(d.toString()) > -1 && captioned == false) {
					table += attributes.sum.caption;
					captioned = true;
				} else if (sum.sum_ids.indexOf(d.toString()) > -1) {
					if (sum.var_percent_ids.indexOf(d.toString()) > -1) {
						if (!isNaN(total[d-1]) && !isNaN(total[d-2]) && total[d-1] != '' && total[d-2] != '')
							table += Math.round((parseFloat(total[d-1]) / parseFloat(total[d-2])) * 100 * 10) / 10;
					} else if (sum.calc_var_percent_ids.indexOf(d.toString()) > -1) {
						if (!isNaN(total[d-1]) && !isNaN(total[d-2]) && total[d-1] != '' && total[d-2] != '')
							table += Math.round(((parseFloat(total[d-2]) - parseFloat(total[d-1])) / parseFloat(total[d-1])) * 100 * 10) / 10;
					} else {
						table += total[d].toLocaleString();
					}
					if (types[d] == "%") {
						table += "%";
					}
				}
				table += '</td>';
			}
			table += '</tr></tfoot>';
		}
	}
	table += '</table>';
	if (results['pagination'] !== undefined) {
		table += '';
	}
	return table;
}

function pie(results) {
	//var colors = 
	var content = [];
	for (var i=0; i< results["data"].length; i++) {
		content.push({"label": results["data"][i][0], "value": parseFloat(results["data"][i][1])});
	}

	var pie = new d3pie("pieChart", {
			"header": {
				"title": {
					"fontSize": 24,
					"font": "open sans"
				},
				"subtitle": {
					"color": "#999999",
					"fontSize": 12,
					"font": "open sans"
				},
				"titleSubtitlePadding": 9
			},
			"footer": {
				"color": "#999999",
				"fontSize": 10,
				"font": "open sans",
				"location": "bottom-left"
			},
			"size": {
				"canvasHeight": 400,
				"canvasWidth": 400,
				"pieOuterRadius": "65%"
			},
			"data": {
				"sortOrder": "label-asc",
				"content": content
			},
			"labels": {
				"outer": {
					"pieDistance": 10
				},
				"inner": {
					"hideWhenLessThanPercentage": 3
				},
				"mainLabel": {
					"fontSize": 11
				},
				"percentage": {
					"color": "#ffffff",
					"decimalPlaces": 0
				},
				"value": {
					"color": "#adadad",
					"fontSize": 11
				},
				"lines": {
					"enabled": true,
					"style": "straight"
				}
			},
			"tooltips": {
				"enabled": true,
				"type": "placeholder",
				"string": "{label}: {value}, {percentage}%"
			},
			"effects": {
				"pullOutSegmentOnClick": {
					"effect": "linear",
					"speed": 400,
					"size": 8
				}
			},
			"misc": {
				"gradient": {
					"enabled": true,
					"percentage": 100
				}
			},
			"callbacks": {
        onClickSegment: function(a) {
          //alert("Drilldown test");
        }
      }
	});
}