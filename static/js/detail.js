
// photos_detail
var map;
var marker;
var infoWindow;

function initMap() {
  var gmap = document.getElementById('gmap');
  map = new google.maps.Map(gmap, {
    center: { lat: 52.215933, lng: 19.134422 },
    zoom: 4.0,
    mapTypeId: 'hybrid',
  });

  window.addEventListener('load', function () {
    var place = $("#place_name").text();
    var geocoder = new google.maps.Geocoder();

    geocoder.geocode({
      'address': place,
      'region': 'eu',
    }, function (results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        console.log(results)

        var bounds = new google.maps.LatLngBounds();

        for (var i in results) {
          if (results[0].geometry) {
            var latlng = results[0].geometry.location;
            var address = results[0].formatted_address;
            // 検索結果地が含まれるように範囲を拡大
            bounds.extend(latlng);
            setMarker(latlng);
            setInfoW(place, latlng, address);
            markerEvent();
            // 検索地を中心にMapを表示
            map.setCenter(latlng);
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
}

function setMarker(setplace) {
  marker = new google.maps.Marker({
    position: setplace,
    map: map,
    animation: google.maps.Animation
  });
}

function setInfoW(place, latlng, address) {
  infoWindow = new google.maps.InfoWindow({
    content: address + "<br><a href='http://www.google.com/search?q=" + place + "&tbm=isch' gmap='_blank'>関連画像検索</a>"
  });
}

function markerEvent() {
  marker.addListener('click', function () {
    infoWindow.open(map, marker);
  });
}
