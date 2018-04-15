$(document).ready(function(){
    $('.btn-reload-devices').click(function(){
		$.get( "http://apione.iotku.id/get_device_list", function(data) {
			$('#device-list').empty();
			var json = JSON.parse(data);
			for(var k in json['result']) {
				var li = '<li><a href="/device?device_ip=' + k[0] + '">' + k[1] + '</a></li>';
				$('#device-list').append(li);
			}
		});
    });
});