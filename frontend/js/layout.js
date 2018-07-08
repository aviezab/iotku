/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("sidenav-big").style.width = "175px";
    document.getElementById("main").style.marginLeft = "175px";
    document.getElementById("sidenav-small").style.width = "0px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("sidenav-big").style.width = "0";
    document.getElementById("main").style.marginLeft = "50px";
    document.getElementById("sidenav-small").style.width = "50px";
}

$(document).ready(function () {
	$('#logout').click(function(){
		$.get( disconnect_url, function(result) {
			if (result.result == true){
				window.location.reload(true);
			}
		});
  });
});