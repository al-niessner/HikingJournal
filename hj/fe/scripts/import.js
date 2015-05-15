window.onload = function ()
{
    input_dev_init();
}

function input_dev_change()
{
    console.log ("change");
    console.log (document.getElementById ("input_device").value);
    
    var connection = new XMLHttpRequest();
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            console.log ("got something from the put");
            console.log (connection.responseText);
        }
    }
    connection.open("PUT", "/import/scan" , true);
    connection.send(JSON.stringify ({device:document.getElementById ("input_device").value}));
}
