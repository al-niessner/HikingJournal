
var metadata_count = 0;
var metadata_expected = 0;
var metadata_is_initializing = false;
var metadata_tl = [];
var metadata_wl = [];

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
        if (metadata_is_initializing)
        {
            var all = {'routes':[], 'tracks':[], 'waypts':[]};

            for (i = 0 ; i < metadata_tl.length ; i++)
            { all.tracks.push (metadata_tl[i]); }
            for (i = 0 ; i < metadata_wl.length ; i++)
            { all.waypts.push (metadata_wl[i]); }
            gpsi_init (all);
            metadata_is_initializing = false;
            document.getElementById ("waypt_list").setAttribute ("disabled","");
        }

        document.getElementById ("waiting").setAttribute ("hidden","");
        document.getElementById ("workbench").removeAttribute ("hidden");
    }
}

function metadata_init()
{
    metadata_is_initializing = true;
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
                opts += '<option value="reset">-- RESET --</option><option disabled>forsaken</option>'
                for (i = 0 ; i < data.barren.length ; i++)
                {
                    metadata_tl.push (data.barren[i]);
                    opts += '<option id="' + data.barren[i].fingerprint + '" value="' + data.barren[i].fingerprint + '">' + data.barren[i].label + '</option>';
                }
                opts += '<option disabled>annotated</option>'
                for (i = 0 ; i < data.annotated.length ; i++)
                {
                    metadata_tl.push (data.annotated[i]);
                    opts += '<option id="' + data.annotated[i].fingerprint+ '" value="' + data.annotated[i].fingerprint + '">' + data.annotated[i].label + '</option>';
                }
            }
            else
            {
                for (i = 0 ; i < data.length ; i++)
                {
                    if (lname === "waypt_list") { metadata_wl.push (data[i]); }
                    opts += '<option id="' + data[i].fingerprint + '" value="' + data[i].fingerprint + '">' + data[i].label + '</option>';
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
    var map = document.getElementById ("map");
    var selp = document.getElementById ("photo_list");
    var selt = document.getElementById ("track_list");
    var selw = document.getElementById ("waypt_list");

    if (selt.value === "reset")
    {
        console.log ('   clear content...');
        document.getElementById ("map").innerHTML = "";
        console.log (selw);
        selw.setAttribute ("disabled","");
        for (w = 0 ; w < selw.selectedOptions.length ; w++)
        {selw.selectedOptions[w].selected = false;}
    }
    else
    {
        var connection = new XMLHttpRequest();
        connection.onreadystatechange = function()
        {
            if (connection.readyState == 4 && connection.status == 200)
            {
                var data = JSON.parse (connection.responseText);

                console.log (data)
                for (w = 0 ; w < data.wids.length ; w++)
                {document.getElementById (data.wids[w]).selected = true;}
                map.innerHTML = '<img alt="USGS Map" class="display" src="/metadata/load' + data.map.name + '"/><p>' + data.map.name + '</p>';
                metadata_free();
            }
        }

        metadata_busy(1);
        selw.removeAttribute ("disabled");
        for (w = 0 ; w < selw.selectedOptions.length ; w++)
        {selw.selectedOptions[w].selected = false;}
        connection.open("GET", "/metadata/collate?tid=" + selt.value, true);
        connection.send();
    }
}

function metadata_update()
{
    var data, opt;
    
    if (gpsi_content.routes.length + gpsi_content.tracks.length - 1 < gpsi_index)
    { data = gpsi_content.waypts[gpsi_index - gpsi_content.routes.length - gpsi_content.tracks.length]; }
    else
    {
        if (gpsi_content.routes.length - 1 < gpsi_index)
        { data = gpsi_content.tracks[gpsi_index - gpsi_content.routes.length]; }
        else { data = gpsi_content.routes[gpsi_index]; }
    }

    opt = document.getElementById (data.fingerprint);

    if (opt) { opt.innerHTML = data.label; }
    else { console.log ('metadata_update(): opt is null'); }
}
