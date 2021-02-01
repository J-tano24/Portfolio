
// photos_new
var map;
var marker;
var infoWindow;

function initMap() {
  var gmap = document.getElementById('gmap');
  map = new google.maps.Map(gmap, {
    center: {lat: 52.215933, lng: 19.134422},
    zoom: 3.8,
    mapTypeId: 'hybrid',
  });

  document.getElementById('search').addEventListener('click', function() {
    var place = $('#keyword').val();
    $('#id_place_name').val(place)

    var geocoder = new google.maps.Geocoder();
    
    geocoder.geocode({
      'address': place,
      'region': 'eu',
    }, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        console.log(results)
        
        var bounds = new google.maps.LatLngBounds();

        for (var i in results) {
          if (results[0].geometry) {
            var latlng = results[0].geometry.location;
            var lat = latlng.lat()
            var lng = latlng.lng()
            $('#id_lat').val(lat)
            $('#id_lng').val(lng)
            
            var address = results[0].formatted_address;
            bounds.extend(latlng);
            setMarker(latlng);
            setInfoW(place, latlng, address);
            markerEvent();
          }
        }
      } else if (status == google.maps.GeocoderStatus.ZERO_RESULTS) {
        alert("見つかりません");
      } else {
        console.log(status);
        alert("エラー発生");
      }
    });
    
  });
  
  document.getElementById('clear').addEventListener('click', function() {
    deleteMakers();
  });
}

function setMarker(setplace) {
  deleteMakers();
  marker = new google.maps.Marker({
    position: setplace,
    map: map,
    animation: google.maps.Animation
  });
}

function deleteMakers() {
  if(marker != null){
    marker.setMap(null);
  }
  marker = null;
}

function setInfoW(place, latlng, address) {
  infoWindow = new google.maps.InfoWindow({
    content: address + "<br><a href='http://www.google.com/search?q=" + place + "&tbm=isch' gmap='_blank'>関連画像検索</a>"
  });
}

function markerEvent() {
  marker.addListener('click', function() {
    infoWindow.open(map, marker);
  });
}