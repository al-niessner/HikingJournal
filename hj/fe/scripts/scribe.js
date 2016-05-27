function scribe_cancel()
{
    var sela = document.getElementById ("annot_list");

    document.getElementById ("new_form").setAttribute ("hidden", "");
    for (a = 0 ; a < sela.selectedOptions.length ; a++)
    { sela.selectedOptions[a].selected = false; }
    document.getElementById ("entry_label").value = "";
    document.getElementById ("annot_record").setAttribute ("disabled", "");
    document.getElementById ("workbench").removeAttribute ("hidden");
}

function scribe_init()
{
    var connection = new XMLHttpRequest();

    document.getElementById ("workbench").setAttribute ("hidden", "");
    document.getElementById ("waiting").removeAttribute ("hidden");
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var data = JSON.parse (connection.responseText);
            var ih = '';

            for (a = 0 ; a < data.annots.length ; a++)
            {
                ih += '<option name="' + data.annots[a].fingerprint;
                ih += '">' + data.annots[a].label + '</option>';
            }
            document.getElementById ("annot_list").innerHTML = ih;
            ih = '<option name="__reset__">-- RESET --</option>';
            for (e = 0 ; e < data.entries.length ; e++)
            { 
                ih += '<option name="' + data.entries[e].fingerprint;
                ih += '">' + data.entries[e].label + '</option>';
            }
            document.getElementById ("entry_list").innerHTML = ih;
            document.getElementById ("waiting").setAttribute ("hidden", "");
            document.getElementById ("workbench").removeAttribute ("hidden");
        }
    }
    connection.open("GET", "/scribe/a_and_e", true);
    connection.send();
}

function scribe_new (update)
{
    if (update)
    {
        if (0 < document.getElementById ("entry_label").value.length &&
            0 < document.getElementById ("annot_list").selectedOptions.length)
        { document.getElementById ("annot_record").removeAttribute ("disabled"); }
    }
    else
    {
        document.getElementById ("workbench").setAttribute ("hidden", "");
        document.getElementById ("new_form").removeAttribute ("hidden");
    }
}

function scribe_record()
{
    var connection = new XMLHttpRequest();
    var params = 'label=' + document.getElementById ('entry_label').value;
    var sela = document.getElementById ("annot_list");

    document.getElementById ("new_form").setAttribute ("hidden", "");
    document.getElementById ("waiting").removeAttribute ("hidden");
    params += '&aids=';
    for (a = 0 ; a < sela.selectedOptions.length-1 ; a++)
    { params += sela.selectedOptions[a].getAttribute ("name") + ','; }
     params += sela.selectedOptions[sela.selectedOptions.length-1].getAttribute ("name");
    connection.onreadystatechange = function()
    {
        if (connection.readyState == 4 && connection.status == 200)
        {
            var data = JSON.parse (connection.responseText);

            // FIXME: loop through the options
            //   option.name == fingerprint, then all good
            //   above is never true, append new option
            document.getElementById ("waiting").setAttribute ("hidden", "");
            document.getElementById ("workbench").removeAttribute ("hidden");
            scribe_init();
        }
    }
    connection.open("PUT", "/scribe/new?" + params, true);
    connection.send();
}

function scribe_sels()
{
    console.log ('new selection');
}
