$(document).ready(function(){
    $('.btn-reload-devices').click(function(){
		$.get( "/api/get_device_list", function(data) {
			for(var k in data['result']) {
				
				var li = '<li><a href="/device?device_ip=' + data['result'][k][0] + '">' + data['result'][k][1] + '</a></li>';
				$('#device-list').append(li);
			}
		});
    });
});