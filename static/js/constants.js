// CORE
var register_url;
var connect_url;
var disconnect_url;
var is_logged_in_url;

// USER
var user_email_url;
var user_api_key_url;
var user_time_added_url;
var user_total_device_url;
var device_list_url;

// DEVICE
var device_name_url;
var device_time_added_url;
var device_total_sensor_url;
var device_sensor_list_url;

// SENSOR
var sensor_name_url;
var sensor_time_added_url;
var sensor_data_url;
var sensor_total_data_entry_url;
var sensor_last_data_added_time_url;
var post_sensor_data_url;
$(document).ready(function(){
	jQuery.get( "/api/url", function(data) {
		var result = data.result;

		// CORE
		register_url = result.register;
		connect_url = result.connect;
		disconnect_url = result.disconnect;
		is_logged_in_url = result.is_logged_in;

		// USER
		user_email_url = result.user_email;
		user_api_key_url = result.user_api_key;
		user_time_added_url = result.user_time_added;
		user_total_device_url = result.user_total_device;
		add_device_url = result.add_device;
		remove_device_url = result.remove_device;
		device_list_url = result.device_list;

		// DEVICE
		device_name_url = result.device_name;
		device_time_added_url = result.device_time_added;
		device_total_sensor_url = result.device_total_sensor;
		add_sensor_url = result.add_sensor;
		remove_sensor_url = result.remove_sensor;
		device_sensor_list_url = result.device_sensor_list;

		// SENSOR
		sensor_name_url = result.sensor_name;
		sensor_time_added_url = result.sensor_time_added;
		sensor_data_url = result.sensor_data;
		sensor_total_data_entry_url = result.sensor_total_data_entry;
		sensor_last_data_added_time_url = result.sensor_last_data_added_time;
		post_sensor_data_url = result.post_sensor_data;
	});
});