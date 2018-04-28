$(document).ready(function(){
	$('#account-info-refresh').click(function(){
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
    });
    $('#device-list-refresh').click(function(){
			$.get( device_list_url, function(data) {
				$('#device-list').html("");
				result = data['result']
				if (result.length > 0) {
					$('#device-list-empty').addClass('invisible');
					for(var k in data['result']) {
						var format = '<h2><a href="' + result[k]['device_id'] +'">' + result[k]['device_name'] + '</a></h2>';
						$('#device-list').append(format);
					}
				}
				else {
					$('#device-list-empty').removeClass('invisible');
				}
			});
    });
    $("#device-form").submit(function (event) {
        event.preventDefault();
        var device_name = $("#device-name").val();
        var device_id = $("#device-id").val();        
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
            }
        });
    });
});