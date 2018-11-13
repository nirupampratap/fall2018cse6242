function initMap() {
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 10,
		center: {lat: 33.753, lng: -84.386}
	});
	var geocoder = new google.maps.Geocoder();
}


function geocodeAddress(geocoder, resultsMap, zipcode) {
	geocoder.geocode({'address': zipcode + " us"}, function(results, status) {
		if (status === 'OK') {
			resultsMap.setCenter(results[0].geometry.location);
			var marker = new google.maps.Marker({
				map: resultsMap,
				position: results[0].geometry.location
			});
		} else {
			alert('Geocode was not successful for the following reason: ' + status);
		}
	});
}