////////////////////////////////////////////////////////////////////////////////

var xmlHttp;

function stateCallback() {
	var stat, rstate;
	if( !xmlHttp ) return;

	try {
		rstate = xmlHttp.readyState;
	} catch (err) {
		alert(err);
	}

	switch( rstate )
	{
		// uninitialized
		case 0:
			// loading
		case 1:
			// loaded
		case 2:
			// interactive
		case 3:
			break;
			// complete, so act on response
		case 4:
			// check http status
			try {
				stat = xmlHttp.status;
			}
			catch (err) {
				stat = "xmlHttp.status does not exist";
			}
			if( stat == 200 )    // success
			{
				AJAX_response(xmlHttp.responseText);
			}
			// loading not successfull, e.g. page not available
			else { }
	}
}

function init_AJAX() 
{
	var new_xmlHttp;
	
	try
	{
		// Internet Explorer
		if( window.ActiveXObject )
		{
			for( var i = 5; i; i-- )
			{
				try
				{
					// loading of a newer version of msxml dll (msxml3 - msxml5) failed
					// use fallback solution
					// old style msxml version independent, deprecated
					if( i == 2 ) {
						new_xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
					}
					// try to use the latest msxml dll
					else {
						new_xmlHttp = new ActiveXObject( "Msxml2.XMLHTTP." + i + ".0" );
					}
					break;
				}
				catch( excNotLoadable ) {
					new_xmlHttp = false;
				}
			}
		}
		// Mozilla, Opera und Safari
		else if( window.XMLHttpRequest ) {
			new_xmlHttp = new XMLHttpRequest();
		}
	}
	catch( excNotLoadable ) {
		new_xmlHttp = false;
	}
	
	new_xmlHttp.onreadystatechange = stateCallback;
	
	xmlHttp = new_xmlHttp;
}

function AJAX_get(url) {
	if( xmlHttp ) {
		xmlHttp.abort();
		xmlHttp = false;
	}
	
	init_AJAX();
	xmlHttp.open("GET", url, true);
	xmlHttp.send(null);
}

////////////////////////////////////////////////////////////////////////////////

function setTextById(element, text) {
	document.getElementById(element).firstChild.nodeValue = text;
}


function setControl(dest, plugin, id, group, value) {
	$.get('/?action=command_ng&dest='+dest+
	'&plugin=' +	plugin+
	'&id='+ 		id + 
	'&group='+ 		group + 
	'&value=' +		value );
}

function setControl_bool(dest, plugin, id, group, value) {
	if (value == false)
		setControl(dest, plugin, id, group, 0);
	else
		setControl(dest, plugin, id, group, 1);
}

function setControl_string(dest, plugin, id, group, value) {
	if (value.length < minlength) {
		alert("The input string has to be least"+minlength+" characters!");
						return;
	}
	$.get('/?action=command_ng&dest=' + dest +
	'&plugin=' + plugin+
	'&id=' + id + 
	'&group=' + group + 
	'&value=' + value, 
	function(data){
		alert("Data Loaded: " + data);
	});
}

function setResolution(plugin, controlId, group, value) {
	$.get('/?action=command_ng&dest=0' + // resolution command always goes to the input plugin
	'&plugin=' + plugin+
	'&id'+ controlId + 
	'&group=1'+// IN_CMD_RESOLUTION == 1,		
	'&value=' + value, 
	function(data){
		if (data == 0) {
			$("#statustd").text("Success");
		} else {
			$("#statustd").text("Error: " + data);
		}
	}
			);
}

function addControl(plugin_id, suffix) {
	var dest = suffix=="in"?0:1;
	$.getJSON(suffix+"put_"+plugin_id+".json", function(data) {
		var showLabel = false;
		var panProp = {
			'found': false,
		   'id': -1,
		   'group': -1
		};
		
		var tiltProp = {
			'found': false,
		   'id': -1,
		   'group': -1
		};
		
		$.each(data.controls, function(i,item){
			$('<tr/>').attr("id", "tr_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id).appendTo("#controltable_"+suffix+"-"+plugin_id);
			
			// BUTTON type controls does not have a label
			if (item.type == 4) {
				$("<td/>").appendTo("#tr-"+item.id);
			} else {
				if (item.type == 6) { // Class type controls
					$("<td/>").text(item.name)
					.attr("style", "font-weight:bold;")
					.attr("id", "td_label_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id)
					.appendTo("#tr_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id);
					return;
				} else {
					$("<td/>")
					.text(item.name)
					.attr("id", "td_label_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id)
					.appendTo("#tr_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id);
				}
			}
			
			$("<td/>").attr("id", "td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id)
			.appendTo("#tr_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id);
			
			showLabel = true;
			if((item.type == 1) || (item.type == 5)) { // integer type controls
				if ((item.id == 10094852) && (item.group == 1) && (item.dest == 0)) { //V4L2_CID_PAN_RELATIVE
					showLabel = false;
					panProp['found'] = true;
					panProp['group'] = item.group;
					panProp['id'] = item.id;
					$("#td_label_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id).remove();
				} else if ((item.id == 10094853) && (item.group == 1) && (item.dest == 0)){ // V4L2_CID_TILT_RELATIVE
					showLabel = false;
					tiltProp['found'] = true;
					tiltProp['group'] = item.group;
					tiltProp['id'] = item.id;
					$("#td_label_"+suffix+"_"+plugin_id+"_"+item.group+"_"+item.id).remove();
				} else { // another non spec control
					var options = {min: item.min, max: item.max, step: item.step,}
					$("<input/>")
					.attr("value", item.value)
					.attr("id", "spinbox-"+item.id)
					.SpinButton(options)
					.bind("valueChanged", function() {setControl(dest, plugin_id, item.id, item.group, $(this).val());})
					.appendTo("#td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id);
				} 
			} else if (item.type == 2) { // boolean type controls
				if (item.value == "1")
					$("<input/>")
					.attr("type", "checkbox")
					.attr("checked", "checked")
					.change(function(){setControl_bool(dest, plugin_id, item.id, item.group, ($(this).attr("checked")?1:0));})
					.appendTo("#td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id);
				else
					$("<input/>")
					.attr("type", "checkbox")
					.change(function(){setControl_bool(dest, plugin_id, item.id, item.group, ($(this).attr("checked")?1:0));})
					.appendTo("#td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id);
			} else if (item.type == 7) { // string type controls
				$("<input/>").attr("value", item.value).appendTo("#td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id);
			} else if (item.type == 3) { // menu
				$("<select/>")
				.attr("name", "select-"+item.id)
				.attr("id", "menu-"+item.id)
				.attr("style", "width: 100%;")
				.change(function(){setControl(dest, plugin_id, item.id, item.group, $(this).val());})
				.appendTo("#td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id);
				$.each(item.menu, function(val, text) {
					if (item.value == val) {
						$("#menu-"+item.id).append($('<option/>').attr("selected", "selected").val(val).html(text));
					} else {
						$("#menu-"+item.id).append($('<option/>').val(val).html(text));
					}
				});
			} else if (item.type == 4) { // button type
				$("<button/>")
				.attr("type", "button")
				.attr("style", "width: 100%; height: 100%;")
				.text(item.name)
				.click(function(){setControl(dest, plugin_id, item.id, item.group, 0);})
				.appendTo("#td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id);
			} else if (item.type == 7) { // string  type
				$("<input/>")
				.attr("type", "text")
				.attr("maxlength", item.max)
				.change(function(){setControl_string(dest, plugin_id, item.id, item.group, $(this).text());})
				.appendTo("#td_ctrl_"+suffix+"_"+plugin_id+"_"+item.group+"-"+item.id);
			} else {
				alert("Unknown control type: "+item.type);
			}
		}); // control foreach loop
				
				if (panProp['found'] && tiltProp['found']) {
					var ptTable = 
					'<div style="text-align: center;"><table class="pt_table">  \
					<tr>  \
					<td class="pt_td"></td>  \
					<td class="pt_td">  \
					<img src="go-up.png" class="pt_btn" id="pt_up">  \
					</td>  \
					<td class="pt_td"></td>  \
					</tr>  \
					<tr>  \
					<td class="pt_td">  \
					<img src="go-previous.png" class="pt_btn" id="pt_left">  \
					</div>  \
					<td class="pt_td"></td>  \
					<td class="pt_td">  \
					<img src="go-next.png" class="pt_btn" id="pt_right">  \
					</td>  \
					</tr>  \
					<tr>  \
					<td class="pt_td"></td>  \
					<td class="pt_td">  \
					<img src="go-down.png" class="pt_btn" id="pt_down">  \
					</td>  \
					<td class="pt_td"></td>  \
					</tr>  \
					</table></div>';
				$("#controltable_"+suffix+"-"+plugin_id).parent().append(ptTable);
				$("#pt_up").click(function(){
					setControl(dest, plugin_id, tiltProp['id'], tiltProp['group'], -200);
				});
				$("#pt_down").click(function(){
					setControl(dest, plugin_id, tiltProp['id'], tiltProp['group'], 200);
				});
				$("#pt_left").click(function(){
					setControl(dest, plugin_id, panProp['id'], panProp['group'], -200);
				});
				$("#pt_right").click(function(){
					setControl(dest, plugin_id, panProp['id'], panProp['group'], 200);
				});
				
				$('.pt_btn').mouseup(function() {
					$(this).removeClass('pt_btn_pushed');
				});
					
					$('.pt_btn').mousedown(function() {
						$(this).addClass('pt_btn_pushed');
					});
				}
	});
}

function showControls(visible) 
{
	if (visible) {
		$("#tabs").show();
	} else {
		$("#tabs").hide();
	}
}

function fillTabs()
{
	$.getJSON("program.json", function(data) {
		$.each(data.inputs, function(i,input){
			$("<li/>").attr("id", "li_in-"+input.id).appendTo("#ul_tabs");
			$("<a/>").attr("href", "#controldiv_in-"+input.id)
			.text(input.name).appendTo("#li_in-"+input.id);
			$("<div/>").attr("id", "controldiv_in-"+input.id).appendTo("#tabs");
			$("<table/>").attr("id", "controltable_in-"+input.id).appendTo("#controldiv_in-"+input.id);
		});
		
		$.each(data.outputs, function(i,output){
			$("<li/>").attr("id", "li_out-"+output.id).appendTo("#ul_tabs");
			$("<a/>").attr("href", "#controldiv_out-"+output.id)
			.text(output.name).appendTo("#li_out-"+output.id);
			$("<div/>").attr("id", "controldiv_out-"+output.id).appendTo("#tabs");
			$("<table/>").attr("id", "controltable_out-"+output.id).appendTo("#controldiv_out-"+output.id);
		});
		
		$.each(data.inputs, function(i,input){
			addControl(input.id, "in");
		});
		
		$.each(data.outputs, function(i,output){
			addControl(output.id, "out");
		});
		$( "#tabs").tabs();
	});
}

function setImageSize(imageId)
{
	$.getJSON('input_0.json', function(data) {
		$.each(data["formats"], function(index, value) {
			if (value["current"] == "true") {
				var dimensions = value["resolutions"][value["currentResolution"]].split("x"); 
				var height = (parseInt(dimensions[1]) / parseInt(dimensions[0])) * $("#"+imageId).width();
				$("#"+imageId).height(height);
				return false;
			}
		});
	});
}