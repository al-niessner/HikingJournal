function scribe_cancel ()
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

function scribe_record ()
{
    console.log ('record new entry');
}

function scribe_sels()
{
    console.log ('new selection');
}
