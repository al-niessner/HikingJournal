
var ingest_content;
var ingest_index = 0;

function import_advance (direction)
{
    var back = document.getElementById ("back");
    var data;
    var next = document.getElementById ("next");
    var title = "Route";
    var workspace = document.getElementById ("workspace");
    ingest_index += direction

    if (ingest_index === 0) {back.setAttribute ("disabled","");}
    else {back.removeAttribute ("disabled");}

    if (ingest_index === ingest_content.routes.length + ingest_content.tracks.length + ingest_content.waypts.length - 1)
    {next.setAttribute ("disabled","");}
    else {next.removeAttribute ("disabled");}

    console.log (ingest_index);
    if (ingest_content.routes.length + ingest_content.tracks.length - 1 < ingest_index)
    {
        data = ingest_content.waypts[ingest_index - ingest_content.routes.length - ingest_content.tracks.length];
        title = "Waypoint";
    }
    else
    {
        if (ingest_content.routes.length - 1 < ingest_index)
        {
            data = ingest_content.tracks[ingest_index - ingest_content.routes.length];
            title = "Track:";
        }
        else { data = ingest_content.routes[ingest_index]; }
    }
    console.log (data);
}

function import_ingest (clear)
{
    var allow = document.getElementById ("allow");
    var connection = new XMLHttpRequest();
    var data = { move:clear, routes:[], tracks:[], waypts:[] };
    var device = {extras:input_dev_extras(),
                  type:document.getElementById ("input_device").value};
    var returns = ["routes", "tracks", "waypts"];
    var tables = ["routes", "tracks", "waypoints"];
    var update = document.getElementById ("update");
    var waiting = document.getElementById ("waiting");

    for (t = 0 ; t < tables.length ; t++)
    {
        var list = document.getElementById (tables[t]);

        for (o = list.selectedOptions.length - 1; 0 <= o ; o--)
        {
            data[returns[t]].push (list.selectedOptions[o].innerHTML);
            if (clear) { list.removeChild (list.selectedOptions[o]); }
        }
    }
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            ingest_content = JSON.parse (connection.responseText);
            ingest_index = 0;
            import_advance (0);
            waiting.setAttribute ("hidden","");
            allow.removeAttribute ("hidden");
            update.removeAttribute ("hidden");
        }
    }
    allow.setAttribute ("hidden","");
    waiting.removeAttribute ("hidden");
    data.device = device;
    connection.open("PUT", "/import/ingest", true);
    connection.send(JSON.stringify (data));
}

function import_init()
{
    input_dev_init();
}

function import_wipe()
{
    var allow = document.getElementById ("allow");
    var connection = new XMLHttpRequest();
    var device = {extras:input_dev_extras(),
                  type:document.getElementById ("input_device").value};
    var waiting = document.getElementById ("waiting");

    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            waiting.setAttribute ("hidden","");
            allow.removeAttribute ("hidden");
        }
    }
    allow.setAttribute ("hidden","");
    waiting.removeAttribute ("hidden");
    connection.open("PUT", "/import/wipe", true);
    connection.send(JSON.stringify (device));
}

function input_dev_ready()
{
    var allow = document.getElementById ("allow");
    var connection = new XMLHttpRequest();
    var device = {extras:input_dev_extras(),
                  type:document.getElementById ("input_device").value};
    var waiting = document.getElementById ("waiting");

    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var args = ["routes", "tracks", "waypts"];
            var data = JSON.parse (connection.responseText);
            var tables = ["routes", "tracks", "waypoints"];

            for (t = 0 ; t < tables.length ; t++)
            {
                var list = document.getElementById (tables[t]);
                var opts = "";
                
                for (o = 0 ; o < data[args[t]].length ; o++)
                {opts += "<option selected>" + data[args[t]][o] + "</option>";}
                list.innerHTML = opts;
            }
            waiting.setAttribute ("hidden","");
            allow.removeAttribute ("hidden");
        }
    }
    allow.setAttribute ("hidden","");
    waiting.removeAttribute ("hidden");
    connection.open("PUT", "/import/scan", true);
    connection.send(JSON.stringify (device));
}
