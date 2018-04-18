$(document).ready(function(){
    $('.btn-reload-devices').click(function(){
		$.get( "/api/get_device_list", function(data) {
			$('#device-list').empty();
			for(var k in data['result']) {
				var a = '<a href="/device?device_ip=' + data['result'][k]['device_ip'] + '">' + data['result'][k]['device_name'] + '</a>'
				var li = '<li>' +
							a +
						 '</li>';
				$('#device-list').append(li);
			}
		});
    });
});