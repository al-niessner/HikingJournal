
function import_copy (clean)
{
    var data = { clean:clean, routes:[], tracks:[], waypts:[] };
    var returns = ["routes", "tracks", "waypts"];
    var tables = ["routes", "tracks", "waypoints"];

    for (t = 0 ; t < tables.length ; t++)
    {
        var list = document.getElementById (tables[t]);

        for (o = 0 ; o < list.selectedOptions.length ; o++)
        { data[returns[t]].push (list.selectedOptions[o].value); }
    }
}

function import_init()
{
    input_dev_init();
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
                {opts += "<option selected value=" + data[args[t]][o] + ">" + data[args[t]][o] + "</option>";}
            list.innerHTML = opts;
            }
        }
    }
    connection.open("PUT", "/import/scan", true);
    connection.send(JSON.stringify (device));
}
