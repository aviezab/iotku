$(document).ready(function(){
    $('.btn-reload-devices').click(function(){
		$.get( "ajax/test.html", function(data) {
			$('#device-list').empty();
			for(var k in data) {
				var li = '<li><a href="/device?device_ip=' + k[0] + '">' + k[1] + '</a></li>'
				$('#device-list').append(li)
			}
		});
    });
});