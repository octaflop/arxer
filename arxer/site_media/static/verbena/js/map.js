// Custom mapping API calls
// Requires: jQuery
$(document).ready( 
	function () {
		var latlng = new google.maps.LatLng(49.28227, -123.10754);
		var myOptions = {
			zoom: 8,
			center: latlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	});
	
