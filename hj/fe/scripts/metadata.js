
var metadata_count = 0;
var metadata_expected = 0;
var metadata_tl = [];
var metadata_tv = [];
var metadata_wl = [];
var metadata_wv = [];

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
        if (metadata_tv.length === 1)
        { }
        else
        {
            var all = {'routes':[], 'tracks':[], 'waypts':[]};

            for (i = 0 ; i < metadata_tl.length ; i++)
            { all.tracks.push (metadata_tl[i]); }
            for (i = 0 ; i < metadata_wl.length ; i++)
            { all.waypts.push (metadata_wl[i]); }
            gpsi_init (all);
        }

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
                opts += '<option></option><option disabled>forsaken</option>'
                for (i = 0 ; i < data.barren.length ; i++)
                {
                    metadata_tl.push (data.barren[i]);
                    opts += '<option value="' + data.barren[i].fingerprint + '">' + data.barren[i].label + '</option>';
                }
                opts += '<option disabled>annotated</option>'
                for (i = 0 ; i < data.annotated.length ; i++)
                {
                    metadata_tl.push (data.annotated[i]);
                    opts += '<option value="' + data.annotated[i].fingerprint + '">' + data.annotated[i].label + '</option>';
                }
            }
            else
            {
                for (i = 0 ; i < data.length ; i++)
                {
                    if (lname === "waypt_list") { metadata_wl.push (data[i]); }
                    opts += '<option value="' + data[i].fingerprint + '">' + data[i].label + '</option>';
                }
            }

            sel.innerHTML = opts;
            metadata_free();
        }
    }
    connection.open("GET", nname, true);
    connection.send();
}

function metadata_selt()
{
    console.log ("selected a track...");
    var selp = document.getElementById ("photo_list");
    var selt = document.getElementById ("track_list");
    var selw = document.getElementById ("waypt_list");

    if (selt.value === "")
    {
        console.log ('   clear content...');
    }
    else
    {
        console.log (selt.value);
        for (w = 0 ; w < selw.selectedOptions.length ; w++)
        {
            console.log (selw.selectedOptions[w].value);
        }
    }
}
