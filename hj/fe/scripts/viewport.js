
function viewport_init (id)
{
    var connection = new XMLHttpRequest();
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var data = JSON.parse (connection.responseText);
            var mlat = 0.0;
            var mlon = 0.0;
            var pc = [];

            for (i = 0 ; i < data.length ; i++)
            {
                mlat += data[i][0];
                mlon += data[i][1];
                pc.push (new google.maps.LatLng(data[i][0],data[i][1]));
            }
            mlat = mlat / data.length;
            mlon = mlon / data.length;
 
            var center= new google.maps.LatLng(mlat,mlon);
            var myOptions = {
                zoom: 14,
                center: center,
                mapTypeControl: true,
                mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
                navigationControl: true,
                mapTypeId: google.maps.MapTypeId.HYBRID
            }
            var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
            var polyline = new google.maps.Polyline({
                path: pc,
                strokeColor: '#FF00FF',
                strokeOpacity: 1.0,
                strokeWeight: 2,
                editable: true
            });

            polyline.setMap(map);    
        }
    }
    connection.open("GET", "/viewport/fetch?id=" + id, true);
    connection.send();
}
