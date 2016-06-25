
var scribe_seg_data;
var scribe_seg_index = 0;

function scribe_activate_save()
{ document.getElementById ("segment_save").removeAttribute ('disabled'); }

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

function scribe_check_buttons()
{
    if (scribe_seg_index + 1 < scribe_seg_data.length)
    { document.getElementById ("segment_succ").removeAttribute ('disabled'); }
    else
    { document.getElementById ("segment_succ").setAttribute ('disabled',''); }
    
    if (0 <= scribe_seg_index - 1)
    { document.getElementById ("segment_prev").removeAttribute ('disabled'); }
    else
    { document.getElementById ("segment_prev").setAttribute ('disabled',''); }
}

function scribe_fill (entry)
{
    var form = '<div><table><caption style="text-align:left;font-weight: bold;">Entry Information</caption>'

    scribe_seg_data = entry;
    scribe_seg_index = 0;
    form += '<tr><td align="right">Segment : </td><td id="segment_number">';
    form += '1 of ' + entry.segs.length;
    form += '</td></tr>';
    form += '<tr><td align="right">Modified Date : </td><td>';
    form += entry.mdate;
    form += '</td></tr>';
    form += '<tr><td align="right">View : </td><td><a href="/viewport/open?id=';
    form += entry.id;
    form += '" target="_blank">All</a></td></tr></table></div>';
    form += '<form><fieldset><legend>Segment</legend>';
    form += '<div><table><caption style="text-align:left;font-weight: bold;">Prologue</caption>'
    form += '<tr><td align="right">Label : </td><td id="segment_label"></td></tr>';
    form += '<tr><td align="right">Date : </td><td id="segment_date"></td></tr>';
    form += '<tr><td align="right">Trailhead : </td><td id="segment_th"></td></tr>';
    form += '<tr><td align="right">Trailend : </td><td id="segment_te"></td></tr>';
    form += '<tr><td align="right">Distance Delta: </td><td id="segment_delta"></td></tr>';
    form += '<tr><td align="right">Distance Walked: </td><td id="segment_walked"></td></tr>';
    form += '<tr><td align="right">Elevation Change : </td><td id="segment_change"></td></tr>';
    form += '<tr><td align="right">Elevation Gain : </td><td id="segment_gain"></td></tr>';
    form += '<tr><td align="right">View : </td><td id="segment_view"></td></tr>';
    form +='</table></div><div><textarea id="segment_text" oninput="scribe_activate_save();" style="height:50vh; width:99%;"></textarea></div><div>';
    form += '<button disabled id="segment_prev" onclick="scribe_step(-1);" type="button">Previous</button>';
    form += '<button disabled id="segment_succ" onclick="scribe_step(1);" type="button">Successor</button>';
    form += '<button disabled id="segment_save" onclick="scribe_save();" style="margin-left:75px;" type="button">Save</button>';
    form += '</div></fieldset></form></fieldset></form>';
    document.getElementById ("entry_form").innerHTML = form;
    scribe_check_buttons();
    scribe_seg_fill();
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

            document.getElementById ("waiting").setAttribute ("hidden", "");
            document.getElementById ("workbench").removeAttribute ("hidden");
            scribe_init();
        }
    }
    connection.open("PUT", "/scribe/new?" + params, true);
    connection.send();
}

function scribe_seg_fill()
{
    document.getElementById ("segment_label").innerHTML = scribe_seg_data.segs[scribe_seg_index].label;
    document.getElementById ("segment_date").innerHTML = scribe_seg_data.segs[scribe_seg_index].date;
    document.getElementById ("segment_th").innerHTML = scribe_seg_data.segs[scribe_seg_index].th;
    document.getElementById ("segment_te").innerHTML = scribe_seg_data.segs[scribe_seg_index].te;
    document.getElementById ("segment_delta").innerHTML = scribe_seg_data.segs[scribe_seg_index].delta;
    document.getElementById ("segment_walked").innerHTML = scribe_seg_data.segs[scribe_seg_index].walked;
    document.getElementById ("segment_change").innerHTML = scribe_seg_data.segs[scribe_seg_index].change;
    document.getElementById ("segment_gain").innerHTML = scribe_seg_data.segs[scribe_seg_index].gain;
    document.getElementById ("segment_view").innerHTML = '<a href="http:/viewport/open?id=' + scribe_seg_data.segs[scribe_seg_index].tid + '" target="_blank">segment</a>';
    document.getElementById ("segment_text").value = scribe_seg_data.segs[scribe_seg_index].text;
}

function scribe_save()
{
    var connection = new XMLHttpRequest();
    var eid = document.getElementById ("entry_list").selectedOptions[0].getAttribute("name");
    
    scribe_seg_data.segs[scribe_seg_index].text = document.getElementById ("segment_text").value;
    document.getElementById ("segment_save").setAttribute ('disabled','');
    connection.open("PUT", "/scribe/save?eid=" + eid, true);
    connection.send(JSON.stringify (scribe_seg_data));
}

function scribe_sels()
{
    var eid = document.getElementById ("entry_list").selectedOptions[0].getAttribute("name");
    var form = document.getElementById ("entry_form");
    
    if (eid === "__reset__") {  form.innerHTML = ""; }
    else
    {
        var connection = new XMLHttpRequest();
        var params = "eid=" + eid;
        
        form.innerHTML = "<h3>Loading Data...</h3>";
        connection.onreadystatechange = function()
        {
            if (connection.readyState == 4 && connection.status == 200)
            { scribe_fill (JSON.parse (connection.responseText)); }
        }
        connection.open("GET", "/scribe/load?" + params, true);
        connection.send();
    }
}

function scribe_step (step)
{
    scribe_seg_index += step;
    scribe_check_buttons();
    scribe_seg_fill()
}

