
function import_complete() { window.location.pathname = '/pages/metadata'; }

function import_done()
{
    document.getElementById ("allow").setAttribute ("hidden","");
    document.getElementById ("update").setAttribute ("hidden","");
    document.getElementById ("waiting").removeAttribute ("hidden");
}

function import_fetch (clear)
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
            gpsi_init (JSON.parse (connection.responseText));
            waiting.setAttribute ("hidden","");
            allow.removeAttribute ("hidden");
            update.removeAttribute ("hidden");
        }
    }
    allow.setAttribute ("hidden","");
    waiting.removeAttribute ("hidden");
    data.device = device;
    connection.open("PUT", "/import/fetch", true);
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
