
function import_copy (clear)
{
    var connection = new XMLHttpRequest();
    var data = { move:clear, routes:[], tracks:[], waypts:[] };
    var device = {extras:input_dev_extras(),
                  type:document.getElementById ("input_device").value};
    var returns = ["routes", "tracks", "waypts"];
    var tables = ["routes", "tracks", "waypoints"];

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
            console.log ("done moving data...");
        }
    }
    data.device = device;
    connection.open("PUT", "/import/move", true);
    connection.send(JSON.stringify (data));
}

function import_init()
{
    input_dev_init();
}

function import_wipe()
{
    console.log ("Wipe the device...");
    var connection = new XMLHttpRequest();
    var device = {extras:input_dev_extras(),
                  type:document.getElementById ("input_device").value};

    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            console.log ("done wiping data...");
        }
    }
    connection.open("PUT", "/import/wipe", true);
    connection.send(JSON.stringify (device));
}

function input_dev_ready()
{
    var connection = new XMLHttpRequest();
    var device = {extras:input_dev_extras(),
                  type:document.getElementById ("input_device").value};

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
            console.log ('scan');
        }
    }
    connection.open("PUT", "/import/scan", true);
    connection.send(JSON.stringify (device));
}
