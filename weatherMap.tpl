<html>
<head>
    <script>
    function moveCloud() {
        var newCords = convertCoordinates(
                parseFloat(document.getElementById('lat').value),
                parseFloat(document.getElementById('lon').value) );
        document.getElementById('cloud').style.left = newCords[0];
        document.getElementById('cloud').style.top = newCords[1];
    }
    function convertCoordinates(lat, lon) {
        var result = new Array();
        const mapWidth = 540;    const mapHeight = 700;
        const leftLon = -10.663; const rightLon = -5.428;
        const topLat = 55.384;   const bottomLat = 51.427;
        const lonRange = Math.abs(leftLon) - Math.abs(rightLon);
        const latRange = Math.abs(topLat) - Math.abs(bottomLat);

        result[0] = Math.round(Math.abs(mapWidth *
                    ((Math.abs(leftLon) - Math.abs(lon)) /
                    lonRange)));
        result[1] = Math.round(Math.abs(mapHeight *
                    ((Math.abs(topLat) - Math.abs(lat)) /
                    latRange)));
        return result
    }
    </script>
</head>
<body style='margin: 0px'>
    <img src='images/ireland.png'>
    <img id='cloud' src='images/cloud.png'
         style='position:absolute; top:100; left:100'>
<div style='position:absolute; top:10; left:10'>
    Latitude: <input type='text' id='lat'><br>
    Longitude: <input type='text' id='lon'><br>
    <button onclick='moveCloud()'>Move Cloud</button>
</div>
</body>
</html>