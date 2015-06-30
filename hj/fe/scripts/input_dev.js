/* load the allowable names for the selection and set the current
   value as selected. */

function input_dev_change()
{
    var connection = new XMLHttpRequest();
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var doc = document.getElementById ("input_device_extras");
            doc.innerHTML = connection.responseText;
            input_dev_ready();
        }
    }
    connection.open("PUT", "/input/extras/" + document.getElementById ("input_device").value, true);
    connection.send();
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

