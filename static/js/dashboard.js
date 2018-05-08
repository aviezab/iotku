var previous_popover;
var delete_device_id;
var sensor_device_id;
var delete_sensor_id;
var rule_device_id;
var rule_sensor_id;
var delete_rule_id;

function hidePopover() {
	$(previous_popover).popover('enable');
	$(previous_popover).popover('hide');
	$(previous_popover).popover('disable');
	previous_popover = null;
}

function accountInfoRefresh() {
	$.get( window.user_email_url, function(data) {
		$("#account-email").text(data.result);
	});
	$.get( window.user_api_key_url, function(data) {
		$("#account-api-key").text(data.result);
	});
	$.get( window.user_time_added_url, function(data) {
		$("#account-registration-date").text(data.result);
	});
	$.get( window.user_total_device_url, function(data) {
		$("#account-total-device").text(data.result);
	});
}

function deviceListRefresh() {
	$.get( user_device_list_url, function(data) {
		$(previous_popover).popover('hide');
		$('#device-list').html('');
		var result = data['result'];
		if (result.length > 0) {
			$('#device-list-error').text('');
			$('#device-list-empty').addClass('d-none');
			for(var k in data['result']) {
				var format = '<div class="row">' + 
				'<button onclick="deviceInfo(this)" type="button" class="btn button-icon device" data-device-id="' + result[k]['device_id']  + '">' + result[k]['device_name'] + '</button>' + 
				'<button onclick="deviceDeletePrompt(this)" type="button" class="btn button-icon device-delete" data-device-id="' + result[k]['device_id']  + '">&times;</button>' + 
				'</div>';
				$('#device-list').append(format);
			}
		}
		else if (result.length == 0) {
			$('#device-list-error').text('');
			$('#device-list-empty').removeClass('d-none');
		}
		else {
			$('#device-list-empty').addClass('d-none');
			$('#device-list-error').text('Error: ' + data.reason);
		}
	});
}

function deviceInfo(element) {
	hidePopover();
	if (previous_popover != element) {
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
		$(element).popover('toggle');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function deviceDeletePrompt(element) {
	delete_device_id = $(element).attr('data-device-id');
	hidePopover();
	if (previous_popover != element) {
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				return $("#device-delete-prompt").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function deviceDeletePromptYes(element) {
	hidePopover();
	$.ajax({
		type: "POST",
		url: user_remove_device_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": delete_device_id
		}),
		success: function(result){
			if (result.result == true) {
				deviceListRefresh();
			}
			else {
				$(element).parents('.device-delete').find('.device-delete-error').text(result.reason);
			}
		}
	});
}

function deviceDeletePromptNo(element){
	hidePopover();
	delete_device_id = null;
}

function sensorListRefresh() {
	$.get( device_sensor_list_url, {device_id: sensor_device_id}, function(data) {
		$(previous_popover).popover('hide');
		$('#sensor-list').html('');
		var result = data['result'];
		if (result.length > 0) {
			$('#sensor-list-error').text('');
			$('#sensor-list-empty').addClass('d-none');
			for(var k in data['result']) {
				var format = '<div class="row">' + 
				'<button onclick="sensorInfo(this)" type="button" class="btn button-icon sensor" data-sensor-id="' + result[k]['sensor_id']  + '">' + result[k]['sensor_name'] + '</button>' + 
				'<button onclick="sensorDeletePrompt(this)" type="button" class="btn button-icon sensor-delete" data-sensor-id="' + result[k]['sensor_id']  + '">&times;</button>' + 
				'</div>';
				$('#sensor-list').append(format);
			}
		}
		else if (result.length == 0) {
			$('#sensor-list-error').text('');
			$('#sensor-list-empty').removeClass('d-none');
		}
		else {
			$('#sensor-list-empty').addClass('d-none');
			$('#sensor-list-error').text('Error: ' + data.reason);
		}
	});
}

function sensorInfo(element) {
	hidePopover();
	if (previous_popover != element) {
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				var sensor_id = $(element).attr('data-sensor-id');
				$(".sensor-id").text(sensor_id);
				$.get( sensor_name_url, {sensor_id: sensor_id, device_id: sensor_device_id}, function(data) {
					$(".sensor-name").text(data.result);
				});
				$.get( sensor_time_added_url, {sensor_id: sensor_id, device_id: sensor_device_id}, function(data) {
					$(".sensor-time-added").text(data.result);
				});
				$.get( sensor_total_data_entry_url, {sensor_id: sensor_id, device_id: sensor_device_id}, function(data) {
					$(".sensor-total-data-entry").text(data.result);
				});
				$.get( sensor_last_data_added_time_url, {sensor_id: sensor_id, device_id: sensor_device_id}, function(data) {
					$(".sensor-last-data-added-time").text(data.result);
				});
				$.get( sensor_total_rule_url, {sensor_id: sensor_id, device_id: sensor_device_id}, function(data) {
					$(".sensor-total-rule").text(data.result);
				});
				return $("#sensor-info").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function sensorDeletePrompt(element) {
	delete_sensor_id = $(element).attr('data-sensor-id');
	hidePopover();
	if (previous_popover != element) {
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				return $("#sensor-delete-prompt").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function sensorDeletePromptYes(element) {
	hidePopover();
	$.ajax({
		type: "POST",
		url: device_remove_sensor_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": sensor_device_id,
			"sensor_id": delete_sensor_id
		}),
		success: function(result){
			if (result.result == true) {
				sensorListRefresh();
			}
			else {
				$(element).parents('.sensor-delete').find('.sensor-delete-error').text(result.reason);
			}
		}
	});
}

function sensorDeletePromptNo(element){
	hidePopover();
	delete_sensor_id = null;
}

function getSensorListFormSubmit(event) {
	event.preventDefault();
	sensor_device_id = $("#get-sensor-list-device-id").val();
	sensorListRefresh();
}

function ruleListRefresh() {
  $.get( sensor_rule_list_url, {device_id: rule_device_id,sensor_id: rule_sensor_id}, function(data) {
    $(previous_popover).popover('hide');
    $('#rule-list').html('');
    var result = data['result'];
    if (result.length > 0) {
      $('#rule-list-error').text('');
      $('#rule-list-empty').addClass('d-none');
      for(var k in data['result']) {
        var format = '<div class="row">' + 
        '<button onclick="ruleInfo(this)" type="button" class="btn button-icon rule" data-rule-id="' + result[k]['rule_id']  + '">' + result[k]['rule_name'] + '</button>' + 
        '<button onclick="ruleDeletePrompt(this)" type="button" class="btn button-icon rule-delete" data-rule-id="' + result[k]['rule_id']  + '">&times;</button>' + 
        '</div>';
        $('#rule-list').append(format);
      }
    }
    else if (result.length == 0) {
      $('#rule-list-error').text('');
      $('#rule-list-empty').removeClass('d-none');
    }
    else {
      $('#rule-list-empty').addClass('d-none');
      $('#rule-list-error').text('Error: ' + data.reason);
    }
  });
}

function ruleInfo(element) {
	hidePopover();
	if (previous_popover != element) {
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				var rule_id = $(element).attr('data-rule-id');
				$(".rule-id").text(rule_id);
				$.get( rule_name_url, {sensor_id: rule_sensor_id, device_id: rule_device_id, rule_id: rule_id}, function(data) {
					$(".rule-name").text(data.result);
				});
				$.get( rule_time_added_url, {sensor_id: rule_sensor_id, device_id: rule_device_id, rule_id: rule_id}, function(data) {
					$(".rule-time-added").text(data.result);
				});
				$.get( rule_expected_value_url, {sensor_id: rule_sensor_id, device_id: rule_device_id, rule_id: rule_id}, function(data) {
					$(".rule-expected-value").text(data.result);
				});
				$.get( rule_operator_url, {sensor_id: rule_sensor_id, device_id: rule_device_id, rule_id: rule_id}, function(data) {
					$(".rule-operator").text(data.result);
				});
				$.get( rule_value_url, {sensor_id: rule_sensor_id, device_id: rule_device_id, rule_id: rule_id}, function(data) {
					$(".rule-value").text(data.result);
				});
				$.get( rule_endpoint_url, {sensor_id: rule_sensor_id, device_id: rule_device_id, rule_id: rule_id}, function(data) {
					$(".rule-endpoint").text(data.result);
				});
				$.get( rule_command_url, {sensor_id: rule_sensor_id, device_id: rule_device_id, rule_id: rule_id}, function(data) {
					$(".rule-command").text(data.result);
				});
				return $("#rule-info").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function ruleDeletePrompt(element) {
	delete_rule_id = $(element).attr('data-rule-id');
	hidePopover();
	if (previous_popover != element) {
		$(element).popover({
			placement:'top',
			html:true,
			content:function(){
				return $("#rule-delete-prompt").html();
			}
		});
		$(element).popover('enable');
		$(element).popover('toggle');
		$(element).popover('disable');
		previous_popover = $(element);
	}
}

function ruleDeletePromptYes(element) {
	hidePopover();
	$.ajax({
		type: "POST",
		url: sensor_remove_rule_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": rule_device_id,
			"sensor_id": rule_sensor_id,
			"rule_id": delete_rule_id
		}),
		success: function(result){
			if (result.result == true) {
				ruleListRefresh();
			}
			else {
				$(element).parents('.rule-delete').find('.rule-delete-error').text(result.reason);
			}
		}
	});
}

function sensorDeletePromptNo(element){
	hidePopover();
	delete_sensor_id = null;
}

function getRuleListFormSubmit(event) {
  event.preventDefault();
  rule_device_id = $("#get-rule-list-device-id").val();
  rule_sensor_id = $("#get-rule-list-sensor-id").val();
  ruleListRefresh();
}

function deviceAddFormSubmit (event) {
	event.preventDefault();
	var device_name = $("#device-form-name").val();
	var device_id = $("#device-form-id").val();        
	$.ajax({
		type: "POST",
		url: user_add_device_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": device_id,
			"device_name": device_name
		}),
		success: function(result){
			if (result.result == true) {
				$('.modal').modal('hide');
				deviceListRefresh();
			}
			else {
				$('#device-form-error').text(result.reason);
			}
		}
	});
}

function sensorAddFormSubmit (event) {
	event.preventDefault();
	var device_id = $("#sensor-form-device-id").val();
	var sensor_name = $("#sensor-form-name").val();
	var sensor_id = $("#sensor-form-id").val();        
	$.ajax({
		type: "POST",
		url: device_add_sensor_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": device_id,
			"sensor_id": sensor_id,
			"sensor_name": sensor_name
		}),
		success: function(result){
			if (result.result == true) {
				$('.modal').modal('hide');
				sensorListRefresh();
			}
			else {
				$('#sensor-form-error').text(result.reason);
			}
		}
	});
}

function ruleAddFormSubmit (event) {
	event.preventDefault();
	var device_id = $("#rule-form-device-id").val();
	var sensor_id = $("#rule-form-sensor-id").val();
	var rule_id = $("#rule-form-id").val();
	var rule_name = $("#rule-form-name").val();
	var rule_expected_value = $("#rule-form-expected-value").val();
	var rule_operator = $("#rule-form-operator").val();
	var rule_value = $("#rule-form-value").val();
	var rule_endpoint = $("#rule-form-endpoint").val();
	var rule_command = $("#rule-form-command").val();
	$.ajax({
		type: "POST",
		url: sensor_add_rule_url,
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({
			"device_id": device_id,
			"sensor_id": sensor_id,
			"rule_id": rule_id,
			"rule_name": rule_name,
			"expected_value": rule_expected_value,
			"operator": rule_operator,
			"value": rule_value,
			"endpoint": rule_endpoint,
			"command": rule_command
		}),
		success: function(result){
			if (result.result == true) {
				$('.modal').modal('hide');
				ruleListRefresh();
			}
			else {
				$('#rule-form-error').text(result.reason);
			}
		}
	});
}

$(document).ready(function(){
	accountInfoRefresh();
	deviceListRefresh();
});