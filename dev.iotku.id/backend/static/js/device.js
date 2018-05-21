$(document).ready(function(){
    $('.btn-reload-devices').click(function(){
		$.get( "/api/get_device_list", function(data) {
			for(var k in data['result']) {
				var format = '<tr>' +
								'<td><a href="' + data['result'][k]['sensor_id'] +'">' + data['result'][k]['sensor_name'] + '</a></td>' +
								'<td>' + data['result'][k]['time_added'] + '</td>' +
								'<td>' +
								  '<a href="#"><span class="glyphicon glyphicon-edit"></span></a>' +
								  '<a href="#"><span class="glyphicon glyphicon-trash"></span></a>' +
								'</td>' +
							 '</tr>';
				$('#device-list').append(li);
			}
		});
    });
});