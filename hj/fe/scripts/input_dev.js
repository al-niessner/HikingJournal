
function input_bool_handler()
{ this.value = (!Boolean(this.value === "true")).toString(); }

function input_dev_change()
{
    var connection = new XMLHttpRequest();
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var doc = document.getElementById ("input_device_extras");

            if (0 < connection.responseText.length)
            { doc.innerHTML = "<form>" + connection.responseText + '<button onclick="input_dev_ready();" type="button">Scan</form>'; }
            input_dev_ready();
        }
    }
    connection.open("PUT", "/input/extras/" + document.getElementById ("input_device").value, true);
    connection.send();
}

function input_dev_extras()
{
    var doc = document.getElementById ("input_device_extras");
    var extras = {};

    for (c = 0 ; c < doc.children.length ; c++)
    {
        if (doc.children[c].hasAttribute ("name"))
        {extras[doc.children[c].name] = doc.children[c].value;}
    }
    return extras;
}

function input_dev_init()
{
    var connection = new XMLHttpRequest();
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var devices = JSON.parse(connection.responseText);
            var opts = "";
            for (i=0 ; i < devices.all.length ; i++)
            {
                if (devices.all[i] === devices.current)
                { opts += '<option selected value="' + devices.all[i] + '">' + devices.all[i] + "</option>"; }
                else
                { opts += '<option value="' + devices.all[i] + '">' + devices.all[i] + "</option>"; }
            }
            document.getElementById ("input_device").innerHTML = opts;
            document.getElementById ("input_device").value = devices.current;
            input_dev_change();
        }
    }
    connection.open("GET", "/input/device" , true);
    connection.send();
}

