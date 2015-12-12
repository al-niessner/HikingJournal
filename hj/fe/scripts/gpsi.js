
var gpsi_content;
var gpsi_index = 0;

function gpsi_advance (direction)
{
    var back = document.getElementById ("back");
    var data;
    var next = document.getElementById ("next");
    var title = "Route";
    var workspace = document.getElementById ("workspace");
    gpsi_index += direction

    if (gpsi_index === 0) {back.setAttribute ("disabled","");}
    else {back.removeAttribute ("disabled");}

    if (gpsi_index === gpsi_content.routes.length + gpsi_content.tracks.length + gpsi_content.waypts.length - 1)
    {next.setAttribute ("disabled","");}
    else {next.removeAttribute ("disabled");}

    if (gpsi_content.routes.length + gpsi_content.tracks.length - 1 < gpsi_index)
    {
        data = gpsi_content.waypts[gpsi_index - gpsi_content.routes.length - gpsi_content.tracks.length];
        title = "Waypoint";
    }
    else
    {
        if (gpsi_content.routes.length - 1 < gpsi_index)
        {
            data = gpsi_content.tracks[gpsi_index - gpsi_content.routes.length];
            title = "Track:";
        }
        else { data = gpsi_content.routes[gpsi_index]; }
    }

    var block = '<p style="margin:0;"><b>' + title + "</b></p>";

    block += '<p style="color:DarkGray;margin:0;text-indent:25px;"><small>device file name: ' + data.name + '</small></p>';
    block += '<p style="margin:0;text-indent:25px;"><a href="/viewport/open?id=' + data.fingerprint + '" target="_blank">View Data</a></p>'
    block += '<br/><label>Label:</label><input id="label_input" style="margin-right:10%; margin-left:1%;" size="80%" type="text" value="' + data.label + '"><br>'
    block += '<label>Description:</label><textarea id="descr_input" style="margin-right:10%; margin-left:5%;" rows="10" cols="80%">' + data.description + '</textarea>'
    workspace.innerHTML = block;
}

function gpsi_ingest()
{
    var connection = new XMLHttpRequest();

    connection.open("PUT", "/import/ingest", true);
    connection.send(JSON.stringify (gpsi_content));
}

function gpsi_init (item_list)
{
    gpsi_content = item_list;
    gpsi_index = 0;
    gpsi_advance (0);
}

function gpsi_record()
{
    var data;
    var description = document.getElementById ("descr_input");
    var label = document.getElementById ("label_input");
    
    if (gpsi_content.routes.length + gpsi_content.tracks.length - 1 < gpsi_index)
    {data = gpsi_content.waypts[gpsi_index - gpsi_content.routes.length - gpsi_content.tracks.length];}
    else
    {
        if (gpsi_content.routes.length - 1 < gpsi_index)
        {data = gpsi_content.tracks[gpsi_index - gpsi_content.routes.length];}
        else {data = gpsi_content.routes[gpsi_index];}
    }

    data.label = label.value;
    data.description = description.value;
}

function gpsi_skip_to (id)
{
    var data;
    for (i = 0 ; i < (gpsi_content.routes.length + gpsi_content.tracks.length +
                      gpsi_content.waypts.length) ; i++)
    {
        if (gpsi_content.routes.length + gpsi_content.tracks.length - 1 < i)
        {
            data = gpsi_content.waypts[i - gpsi_content.routes.length - gpsi_content.tracks.length];
        }
        else
        {
            if (gpsi_content.routes.length - 1 < i)
            {
                data = gpsi_content.tracks[i - gpsi_content.routes.length];
            }
            else { data = gpsi_content.routes[i]; }
        }

        if (data.fingerprint === id)
        {
            gpsi_index = i;
            gpsi_advance (0);
            i = (gpsi_content.routes.length + gpsi_content.tracks.length +
                 gpsi_content.waypts.length) + 1;
        }
    }
}
