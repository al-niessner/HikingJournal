
var metadata_count = 0;
var metadata_expected = 0;

function metadata_busy (expected)
{
    metadata_count = 0;
    metadata_expected = expected;
    document.getElementById ("workbench").setAttribute ("hidden","");
    document.getElementById ("waiting").removeAttribute ("hidden");
}

function metadata_free()
{
    metadata_count++;

    if (metadata_expected <= metadata_count)
    {
        document.getElementById ("waiting").setAttribute ("hidden","");
        document.getElementById ("workbench").removeAttribute ("hidden");
    }
}

function metadata_init()
{
    metadata_busy (3);
    metadata_load ("photo_list", "/metadata/photos");
    metadata_load ("track_list", "/metadata/tracks");
    metadata_load ("waypt_list", "/metadata/waypts");
}

function metadata_load (lname, nname)
{
    var connection = new XMLHttpRequest();
    var sel = document.getElementById (lname);
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var data = JSON.parse (connection.responseText);
            var opts = ""

            if (lname === "track_list")
            {
                opts += '<option disabled>forsaken</option>'
                for (i = 0 ; i < data.barren.length ; i++)
                { opts += '<option value="' + data.barren[i].fingerprint + '">' + data.barren[i].label + '</option>'; }
                opts += '<option disabled>annotated</option>'
                for (i = 0 ; i < data.annotated.length ; i++)
                { opts += '<option value="' + data.annotated[i].fingerprint + '">' + data.annotated[i].label + '</option>'; }
            }
            else
            {
                for (i = 0 ; i < data.length ; i++)
                { opts += '<option value="' + data[i].fingerprint + '">' + data[i].label + '</option>'; }
            }

            sel.innerHTML = opts;
            metadata_free();
        }
    }
    connection.open("GET", nname, true);
    connection.send();
}
