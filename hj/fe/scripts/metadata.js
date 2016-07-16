
var metadata_count = 0;
var metadata_expected = 0;
var metadata_facets = [];
var metadata_is_initializing = false;
var metadata_tl = [];
var metadata_wl = [];

function metadata_assign()
{
    var connection = new XMLHttpRequest();
    var maps = document.getElementById ("stiched_maps");
    var params = "";
    var selp = document.getElementById ("photo_list");
    var selt = document.getElementById ("track_list");
    var selw = document.getElementById ("waypt_list");

    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            metadata_free();
        }
    }
    params += "tid=" + selt.value;
    
    if (maps === null) {}
    else {params += "&mid=" + maps.name;}

    if (0 < selp.selectedOptions.length)
    {
        params += "&pids="
        for (p = 0 ; p < selp.selectedOptions.length ; p++)
        {
            params += selp.selectedOptions[p].id;
            if (p < selp.selectedOptions.length-1) params += ':';
        }
    }

    if (0 < selw.selectedOptions.length)
    {
        params += "&wids="
        for (w = 0 ; w < selw.selectedOptions.length ; w++)
        {
            params += selw.selectedOptions[w].id;
            if (w <  selw.selectedOptions.length-1) params += ":";
        }
    }

    metadata_busy(1);
    connection.open("PUT", "/metadata/assign?" + params, true);
    connection.send(JSON.stringify (metadata_facets));
}

function metadata_busy (expected)
{
    metadata_count = 0;
    metadata_expected = expected;
    document.getElementById ("add_popup").setAttribute ("hidden","");
    document.getElementById ("workbench").setAttribute ("hidden","");
    document.getElementById ("waiting").removeAttribute ("hidden");
}

function metadata_facet_add (key, value)
{
    document.getElementById ("add_popup").removeAttribute ("hidden");
    document.getElementById ("waiting").setAttribute ("hidden","");
    document.getElementById ("workbench").setAttribute ("hidden","");
    document.getElementById ("input_key").value = key;
    document.getElementById ("input_value").value = value;
}

function metadata_facet_done (record)
{
    if (record)
    {
        metadata_facets.push ({'key':document.getElementById ("input_key").value,
                               'value':document.getElementById ("input_value").value});
        metadata_facet_update();
    }
    
    document.getElementById ("add_popup").setAttribute ("hidden","");
    document.getElementById ("waiting").setAttribute ("hidden","");
    document.getElementById ("workbench").removeAttribute ("hidden");
}

function metadata_facet_edit()
{
    var self = document.getElementById ("facet_list");
    var val = "";
    
    for (i = 0 ; i < metadata_facets.length ; i++)
    { if (self.value === metadata_facets[i]) { val = metadata_facets[i]; } }
    metadata_facet_add (self.value, val);
}

function metadata_facet_remove()
{
    var list = [];
    var self = document.getElementById ("facet_list");

    for (f = 0 ; f < metadata_facets.length ; f++)
    {
        if (metadata_facets[f].key === self.value) {}
        else { list.push (metadata_facets[f]); }
    }
    metadata_facets = list;
    metadata_facet_update();
    console.log (self.value);
}

function metadata_facet_update()
{
    var dele = document.getElementById ("facet_remove");
    var edit = document.getElementById ("facet_edit");
    var label = document.getElementById ("facet_value");
    var opts = "";
    var self = document.getElementById ("facet_list");
    
    for (i = 0 ; i < metadata_facets.length ; i++)
    { opts += "<option>" + metadata_facets[i].key + "</option>"; }
    
    if (0 < metadata_facets.length)
    {
        dele.removeAttribute ("disabled");
        edit.removeAttribute ("disabled");
        label.innerHTML = metadata_facets[0].value;
    }
    else
    {
        dele.setAttribute ("disabled","");
        edit.setAttribute ("disabled","");
        label.innerHTML = "";
    }

    self.innerHTML = opts;
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

        document.getElementById ("add_popup").setAttribute ("hidden","");
        document.getElementById ("waiting").setAttribute ("hidden","");
        document.getElementById ("workbench").removeAttribute ("hidden");
    }
}

function metadata_init()
{
    metadata_is_initializing = true;
    metadata_busy (3);
    document.getElementById ("facet_edit").setAttribute ("disabled","");
    document.getElementById ("facet_list").innerHTML = "";
    document.getElementById ("facet_remove").setAttribute ("disabled","");
    document.getElementById ("facet_value").innerHTML = "";
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
                opts += '<option value="reset">-- RESET --</option><optgroup label="forsaken">'
                for (i = 0 ; i < data.barren.length ; i++)
                {
                    metadata_tl.push (data.barren[i]);
                    opts += '<option id="' + data.barren[i].fingerprint + '" value="' + data.barren[i].fingerprint + '">' + data.barren[i].label + '</option>';
                }
                opts += '</optgroup><optgroup label="annotated">';
                for (i = 0 ; i < data.annotated.length ; i++)
                {
                    metadata_tl.push (data.annotated[i]);
                    opts += '<option id="' + data.annotated[i].fingerprint+ '" value="' + data.annotated[i].fingerprint + '">' + data.annotated[i].label + '</option>';
                }
                opts += '</optgroup>';
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

function metadata_self()
{
    var self = document.getElementById ("facet_list");

    for (f = 0 ; f < metadata_facets.length ; f++)
    { if (self.value === metadata_facets[f].key) document.getElementById ("facet_value").innerHTML = metadata_facets[f].value; }
}

function metadata_selt()
{
    var done = document.getElementById ("done_button");
    var map = document.getElementById ("map");
    var selp = document.getElementById ("photo_list");
    var selt = document.getElementById ("track_list");
    var selw = document.getElementById ("waypt_list");

    if (selt.value === "reset")
    {
        done.setAttribute ("disabled","");
        map.innerHTML = "";
        selw.setAttribute ("disabled","");
        for (w = 0 ; w < selw.selectedOptions.length ; w++)
        {selw.selectedOptions[w].selected = false;}
        document.getElementById ("facet_edit").setAttribute ("disabled","");
        document.getElementById ("facet_list").innerHTML = "";
        document.getElementById ("facet_remove").setAttribute ("disabled","");
        document.getElementById ("facet_value").innerHTML = "";
    }
    else
    {
        var connection = new XMLHttpRequest();
        var fconnection = new XMLHttpRequest();

        connection.onreadystatechange = function()
        {
            if (connection.readyState == 4 && connection.status == 200)
            {
                var data = JSON.parse (connection.responseText);

                for (w = 0 ; w < data.wids.length ; w++)
                {document.getElementById (data.wids[w]).selected = true;}
                gpsi_record();
                gpsi_skip_to (selt.value);

                if ('name' in data.map)
                {
                    // Seems that <map> does not handle images being scaled
                    // very gracefully. Need to find another solution...
                    var cmap = '<map name="USGS_WAYPTS">';

                    for (w = 0 ; w < data.map.waypts.length ; w++)
                    {
                        cmap += '<area title="WayPoint" shape="circle" coords="';
                        cmap += data.map.waypts[w][1];
                        cmap += ',';
                        cmap += data.map.waypts[w][0];
                        cmap += ',100" onclick="gpsi_skip_to (\'';
                        cmap += data.wids[w];
                        cmap += '\');">';
                    } 
                    cmap += '</map>';
                    map.innerHTML = '<img alt="USGS Map" class="display" id="stiched_maps" name="' + data.map.fingerprint + '" src="/metadata/load' + data.map.name + '" usemap="#USGS_WAYPTS"/><button id="external_viewer" name="' + data.map.name + '" onclick="metadata_spawn();" type="button">External Viewer</button>' + cmap;
                    console.log (map.innerHTML);
                }
                else
                {
                    if (data.map.constituents.length == 0)
                    {
                        map.innerHTML = '<h4>No maps for this area</h4>';
                    }
                    else
                    {
                        var clist = '<h4>Some data is contained within:</h4><ul>';

                        for (i = 0 ; i < data.map.constituents.length ; i++)
                        {clist += '<li>' + data.map.constituents[i] + '</li>';}
                        clist += '</ul>';
                        map.innerHTML = clist;
                    }
                }
                done.removeAttribute ("disabled");
                selw.removeAttribute ("disabled");
                console.log ("end of get track data");
                metadata_free();
            }
        }

        fconnection.onreadystatechange = function()
        {
            if (fconnection.readyState == 4 && fconnection.status == 200)
            {
                var data = JSON.parse (fconnection.responseText);

                metadata_facets = data;
                metadata_facet_update();
                metadata_free();
                console.log ("end of get facets");
            }
        }
        
        metadata_busy(2);
        for (w = 0 ; w < selw.selectedOptions.length ; w++)
        {selw.selectedOptions[w].selected = false;}
        connection.open("GET", "/metadata/collate?tid=" + selt.value, true);
        connection.send();
        fconnection.open("GET", "/metadata/facets?tid=" + selt.value, true);
        fconnection.send();
    }
}

function metadata_spawn()
{
    var connection = new XMLHttpRequest();
    var spawn = document.getElementById ("external_viewer");
    connection.open("PUT", "/metadata/spawn" + spawn.name, true);
    connection.send();
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
