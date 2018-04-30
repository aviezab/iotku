var previous_popover;
var delete_device_id;
var sensor_device_id;
var delete_sensor_id;


function accountInfoRefresh() {
	$.get( user_email_url, function(data) {
		$("#account-email").text(data.result);
	});
	$.get( user_api_key_url, function(data) {
		$("#account-api-key").text(data.result);
	});
	$.get( user_time_added_url, function(data) {
		$("#account-registration-date").text(data.result);
	});
	$.get( user_total_device_url, function(data) {
		$("#account-total-device").text(data.result);
	});
}

function deviceListRefresh() {
	$.get( device_list_url, function(data) {
		$(previous_popover).popover('hide');
		$('#device-list').html('');
		result = data['result']
		if (result.length > 0) {
			$('#device-list-error').text('');
			$('#device-list-empty').addClass('invisible');
			for(var k in data['result']) {
				var format = '<div class="row">' + 
				'<button onclick="deviceInfo(this)" type="button" class="btn button-icon device" data-device-id="' + result[k]['device_id']  + '">' + result[k]['device_name'] + '</button>' + 
				'<button onclick="deviceDeletePrompt(this)" type="button" class="btn button-icon device-delete" data-device-id="' + result[k]['device_id']  + '">&times;</button>' + 
				'</div>';
				$('#device-list').append(format);
			}
		}
		else if (result.length == 0) {
			$('#device-list-empty').removeClass('invisible');
		}
		else {
			$('#device-list-error').text('Error: ' + data.reason);
		}
	});
}

function deviceInfo(element) {
	if (previous_popover == element) {
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
	}
	else {
		$(previous_popover).popover('enable');
		$(previous_popover).popover('hide');
		$(previous_popover).popover('disable');
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				var device_id = $(element).attr('data-device-id');
				$(".device-id").text(device_id);
				$.get( device_name_url, {device_id: device_id}, function(data) {
					$(".device-name").text(data.result);
				});
				$.get( device_time_added_url, {device_id: device_id}, function(data) {
					$(".device-time-added").text(data.result);
				});
				$.get( device_total_sensor_url, {device_id: device_id}, function(data) {
					$(".device-total-sensor").text(data.result);
				});
				return $("#device-info").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('show');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function deviceDeletePrompt(element) {
	delete_device_id = $(element).attr('data-device-id');
	if (previous_popover == element) {
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
	}
	else {
		$(previous_popover).popover('enable');
		$(previous_popover).popover('hide');
		$(previous_popover).popover('disable');
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				return $("#device-delete-prompt").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('show');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function deviceDeletePromptYes(element) {
	$.ajax({
		type: "POST",
		url: remove_device_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": delete_device_id
		}),
		success: function(result){
			if (result.result == true) {
				window.location.reload(true);
			}
			else {
				$(element).parents('.device-delete').find('.device-delete-error').text(result.reason);
			}
		}
	});
}

function deviceDeletePromptNo(element){
	$(previous_popover).popover('enable');
	$(previous_popover).popover('hide');
	$(previous_popover).popover('disable');
	previous_popover = null;
	delete_device_id = null;
}

function sensorInfo(element) {
	if (previous_popover == element) {
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
	}
	else {
		$(previous_popover).popover('enable');
		$(previous_popover).popover('hide');
		$(previous_popover).popover('disable');
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				var sensor_id = $(element).attr('data-sensor-id');
				$(".sensor-id").text(sensor_id);
				$.get( sensor_name_url, {sensor_id: sensor_id, device_id: device_id}, function(data) {
					$(".sensor-name").text(data.result);
				});
				$.get( sensor_time_added_url, {sensor_id: sensor_id, device_id: device_id}, function(data) {
					$(".sensor-time-added").text(data.result);
				});
				return $("#sensor-info").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('show');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}
function sensorDeletePrompt(element) {
	delete_sensor_id = $(element).attr('data-sensor-id');
	if (previous_popover == element) {
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
	}
	else {
		$(previous_popover).popover('enable');
		$(previous_popover).popover('hide');
		$(previous_popover).popover('disable');
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				return $("#sensor-delete-prompt").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('show');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function sensorDeletePromptYes(element) {
	$.ajax({
		type: "POST",
		url: remove_sensor_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": sensor_device_id,
			"sensor_id": delete_sensor_id
		}),
		success: function(result){
			if (result.result == true) {
				window.location.reload(true);
			}
			else {
				$(element).parents('.sensor-delete').find('.sensor-delete-error').text(result.reason);
			}
		}
	});
}

function sensorDeletePromptNo(element){
	$(previous_popover).popover('enable');
	$(previous_popover).popover('hide');
	$(previous_popover).popover('disable');
	previous_popover = null;
	delete_sensor_id = null;
}

$(document).ready(function(){
	$("#get-sensor-list").submit(function (event) {
		event.preventDefault();   
		$.get( device_sensor_list_url, {device_id: $("#get-sensor-list-device-id").val()}, function(data) {
			$(previous_popover).popover('hide');
			$('#sensor-list').html('');
			result = data['result']
			if (result.length > 0) {
				$('#sensor-list-error').text('');
				$('#sensor-list-empty').addClass('invisible');
				for(var k in data['result']) {
					var format = '<div class="row">' + 
					'<button onclick="sensorInfo(this)" type="button" class="btn button-icon sensor" data-sensor-id="' + result[k]['sensor_id']  + '">' + result[k]['sensor_name'] + '</button>' + 
					'<button onclick="sensorDeletePrompt(this)" type="button" class="btn button-icon sensor-delete" data-sensor-id="' + result[k]['sensor_id']  + '">&times;</button>' + 
					'</div>';
					$('#sensor-list').append(format);
				}
				sensor_device_id = $("#get-sensor-list-device-id").val()
			}
			else if (result.length == 0) {
				$('#sensor-list-empty').removeClass('invisible');
				sensor_device_id = null;
			}
			else {
				$('#sensor-list-empty').addClass('invisible');
				$('#sensor-list-error').text('Error: ' + data.reason);
				sensor_device_id = null;
			}
		});
	});
	$("#device-form").submit(function (event) {
		event.preventDefault();
		var device_name = $("#device-form-name").val();
		var device_id = $("#device-form-id").val();        
		$.ajax({
			type: "POST",
			url: add_device_url,
			contentType: "application/json",
			dataType: "json",
			data: JSON.stringify({
				"device_id": device_id,
				"device_name": device_name
			}),
			success: function(result){
				if (result.result == true) {
					window.location.reload(true);
				}
				else {
					$('#device-form-error').text(result.reason);
				}
			}
		});
	});
	$("#sensor-form").submit(function (event) {
		event.preventDefault();
		var device_id = $("#sensor-form-device-id").val();
		var sensor_name = $("#sensor-form-name").val();
		var sensor_id = $("#sensor-form-id").val();        
		$.ajax({
			type: "POST",
			url: add_sensor_url,
			contentType: "application/json",
			dataType: "json",
			data: JSON.stringify({
				"device_id": device_id,
				"sensor_id": sensor_id,
				"sensor_name": sensor_name
			}),
			success: function(result){
				if (result.result == true) {
					window.location.reload(true);
				}
				else {
					$('#sensor-form-error').text(result.reason);
				}
			}
		});
	});
});