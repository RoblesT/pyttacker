var pyttacker = false;
var busy = false;
var poc_list=[];

//Crear objetos Ajax
function nuevoAjax(){
	var xmlhttp=false;
 	try {
 		xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
 	} catch (e) {
 		try {
 			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
 		} catch (E) {
 			xmlhttp = false;
 		}
  	}

	if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
 		xmlhttp = new XMLHttpRequest();
	}
	return xmlhttp;
}


function load_plugin(pid){
	var query, contenedor;
	contenedor = document.getElementById('results');
	if (contenedor != null && pyttacker) {
		postdata="plugin="+pid+"&action=get_info";
		ajax=nuevoAjax();
		ajax.open("POST", "/",true);
		ajax.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		contenedor.innerHTML = 'Working, please wait!';
		ajax.onreadystatechange=function() {
			if (ajax.readyState==4) {
				response = ajax.responseText;
				busy=false;
				poc='';
				message='';
				action='';
				data='';
				
				list=response.split('<|>');
				for (index = 0; index < list.length; ++index) {
					key=list[index].split('<=>');
					switch (key[0]){
					//'poc':'','message':'','action':'','data'
					case 'poc':
						poc=key[1];
						break;
					case 'action':
						action=key[1];
						tmp=action.split('<;>');
						clear_poc();
						for (i = 0; i < tmp.length; ++i) {
							if (tmp[i]!=''){
								t=tmp[i].split("<:>");
								if (t.length == 4){
									if (t[0]!='' && t[1]!=''){
										add_poc(t[0],t[1],t[2],t[3]);
									}
								}
							}
						}
						break;
					case 'data':
						data=key[1];
						tmp=data.split('<;>');
						for (i = 0; i < tmp.length; ++i) {
							if (tmp!=''){
								t=tmp[i].split("<:>",2);
								switch (t[0]){
								case 'name':
									document.getElementById("plugin_name").innerHTML=t[1];
									break;
								case 'description':
									document.getElementById("plugin_description").innerHTML=t[1];
									break;
								case 'author':
									document.getElementById("plugin_author").innerHTML=t[1];
									break;
								}
							}
						}
						break;
					}
				}
				if (poc == 'true'){
					contenedor.innerHTML = "<span style='color:green;'>Process completed</span>";
					poc_change();
				}else if (poc == 'error'){
					contenedor.innerHTML = "<span style='color:red;'>An internal error happened, please check Pyttacker output log in the console</span>";
				}else if (poc == 'false'){
					contenedor.innerHTML = "<span style='color:green;'>"+message+"</span>";
				}
			}
		}
		busy=true;
		ajax.send(postdata)
	}
}

function load_poc(pid){
	for (index = 0; index < poc_list.length; ++index) {
		if (poc_list[index].id == pid){
			document.getElementById('poc_name').innerHTML = poc_list[index].name;
			document.getElementById('poc_payload').innerHTML = poc_list[index].payload;
		}
	}	
}
function get_payload(poc){
	for (index = 0; index < poc_list.length; ++index) {
		if (poc_list[index].id == poc){
			return poc_list[index].payload;
		}
	}
}
function get_client_action(poc){
	for (index = 0; index < poc_list.length; ++index) {
		if (poc_list[index].id == poc){
			return poc_list[index].action;
		}
	}
}

function service_status(){
	var query, contenedor;
	contenedor = document.getElementById('status');
	if (contenedor != null && !busy) {
		postdata="action=you_ok?";
		ajax=nuevoAjax();
		ajax.open("POST", "/",true);
		ajax.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		contenedor.innerHTML = '...';
		ajax.onreadystatechange=function() {
			if (ajax.readyState==4) {
				response = ajax.responseText;
				if (response == 'yes'){
					contenedor.innerHTML = "<span style='color:green;'>Server Online</span>";
					document.getElementById("cmd_send").disabled = false;
					pyttacker = true;
				}else{
					contenedor.innerHTML = "<span style='color:red;'>Server offline</span>";
					document.getElementById("cmd_send").disabled = true;
					pyttacker = false;
				}
			}
		}
		ajax.send(postdata)
	}
}
function clear_poc()
{
    var i;
    poc_list.length = 0;
    selectbox=document.getElementById("cmb_poc")
    for(i=selectbox.options.length-1;i>=0;i--)
    {
        selectbox.remove(i);
    }
}
function add_poc(value,text, client_action, payload){
	var select = document.getElementById("cmb_poc");
	select.options[select.options.length] = new Option(text, value);
	poc_list.push({
	    id:   value,
	    name: text,
	    action: client_action,
	    payload: payload
	});
}
function send_to_pyttacker(){
	var query, contenedor, plugin, poc, idpoc;
	contenedor = document.getElementById('results');
	url=document.getElementById('idurl').value;
	var e = document.getElementById("cmb_plugin");
	if( e.options[e.selectedIndex].value != ''){ plugin= e.options[e.selectedIndex].value;}
	e = document.getElementById("cmb_poc");
	if( e.options[e.selectedIndex].value != ''){ idpoc= e.options[e.selectedIndex].value;}
	pdata=document.getElementById("iddata").value;
	
	postdata="plugin="+plugin+"&action="+idpoc+"&url="+url+"&postdata="+escape(pdata);
	if (contenedor != null) {
		query = url;
		ajax=nuevoAjax();
		ajax.open("POST", "/",true);
		ajax.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		contenedor.innerHTML = 'Working, please wait!';
		ajax.onreadystatechange=function() {
			if (ajax.readyState==4) {
				response = ajax.responseText;
				poc='';
				message='';
				action='';
				data='';
				list=response.split('<|>');
				for (index = 0; index < list.length; ++index) {
					key=list[index].split('<=>');
					switch (key[0]){
					//'poc':'','message':'','action':'','data'
					case 'poc':
						poc=key[1]
						break;
					case 'message':
						message=key[1]
						break;
					case 'action':
						action=key[1]
						break;
					case 'data':
						data=key[1]
						break;
					}
				}
				if (poc == 'true'){
					switch (action){
					case 'go':
						send_request(document.getElementById('idurl').value,document.getElementById('iddata').value);
						break;
					case 'go_payload':
						url=get_payload(idpoc);
						send_request(url,data);
						break;
					}
					contenedor.innerHTML = "<span style='color:red;'>"+message+"</span>";
				}else if (poc == 'error'){
					contenedor.innerHTML = "<span style='color:red;'>An internal error happened, please check Pyttacker output log in the console</span>";
				}else if (poc == 'false'){
					contenedor.innerHTML = "<span style='color:green;'>"+message+"</span>";
				}
			}
		}
		ajax.send(postdata)
	}

}
function resetiFrame() { 
   	ifrm = document.getElementById("attack_frame");
	if (ifrm){
		removeElement("attack_frame");
	}
	addElementToParent("attack_frame","IFRAME","div_poc");
	ifrm = document.getElementById("attack_frame");
	ifrm.name="attack_frame";
   	ifrm.style.width = 100+"%"; 
   	ifrm.style.height = 60+"%"; 

}
function sendtoiFrame(url) { 
   	
	ifrm = document.getElementById("attack_frame"); 
   	ifrm.setAttribute("src", url); 
	try {
		poc = (ifrm.contentDocument || ifrm.contentWindow);
		if (poc != null){
			poc = '';
		}
	}catch(err){
		poc='<hr/><b>This Browser raised an error while trying to access the iFrame: <br/>'+err+'</b>';
	}
	return poc;
}
function change_action(url,method) {
   	frm = document.getElementById("attack_form"); 
   	frm.setAttribute("action", url);
   	frm.setAttribute("method", method);
	frm.submit();
}
function getmethod(){
	var e = document.getElementById("cmbmethod");    
	return e.options[e.selectedIndex].value;
}

function send_request(url,postdata) {
	
	csrf_form = document.getElementById("csrf_form");
	if (csrf_form){ 
		removeElement("csrf_form");
	}
	if (postdata){method = 'POST';}else{method='GET';}
	if (method == 'POST'){
		addElement("csrf_form","form");
		csrf_form = document.getElementById("csrf_form");
		
		if (csrf_form){
			csrf_form.setAttribute("action", url);
			csrf_form.setAttribute("method", method);
			if (!document.getElementById("idtopopup").checked){
				csrf_form.setAttribute("target", "_blank");
				document.getElementById('results').innerHTML="<span style='color:red;'>Sending POST request directly to a new tab (No server processing)</span>";
			}else{
				poc_window();
				csrf_form.setAttribute("target", "attack_window");
				document.getElementById('results').innerHTML="<span style='color:red;'>Sending POST request directly to a new Window (No server processing)</span>";
			}		
			params = postdata;
			parameters = params.split("&");
			for (i = 0; i < parameters.length; ++i) {
				param = parameters[i].split("=",2);
				addElementToParent('input'+i,'input',"csrf_form")
				input_tag = document.getElementById('input'+i)
				input_tag.setAttribute("type", 'hidden');
				input_tag.setAttribute("name", param[0]);
				input_tag.setAttribute("value", param[1]);
			}
			csrf_form.submit();
		}
	}else{
		if (!document.getElementById("idtopopup").checked){
			new_tab(url);
			document.getElementById('results').innerHTML="<span style='color:red;'>Sending GET request directly to a new tab (No server processing)</span>";
		}else{
			poc_window(url);
			document.getElementById('results').innerHTML="<span style='color:red;'>Sending GET request directly to a new Window (No server processing)</span>";
		}
	}
}


function poc_window(url){
	window.open(url,"attack_window","width=640,height=480");
}
function new_tab(url)
{
  var win=window.open(url, '_blank');
  win.focus();
}
function start(){
	service_status()
	setInterval('service_status()',10000);
	method_change();
	plugin_change();
}
function send(){
	var e = document.getElementById("cmb_plugin");
	plugin=e.options[e.selectedIndex].value
	e = document.getElementById("cmb_poc");
	poc=e.options[e.selectedIndex].value
	action=get_client_action(poc)
	if( plugin != '' && poc != '' && action == 'pyttacker'){
		send_to_pyttacker();
	}else{
		send_request(document.getElementById('idurl').value,document.getElementById('iddata').value);
	}
}
function plugin_change(){
	var e = document.getElementById("cmb_plugin");
	if (e.options[e.selectedIndex].value != ''){
		show_tag('info');
		document.getElementById('poc_name').innerHTML = '';
		document.getElementById('poc_payload').innerHTML = '';
		if (pyttacker){
			load_plugin(e.options[e.selectedIndex].value);
		}
	}else{
		hide_tag('info');
		clear_poc();
	}
}
function poc_change(){
	var e = document.getElementById("cmb_poc");
	if (pyttacker){
		load_poc(e.options[e.selectedIndex].value);
	}
}
function hide_tag(idtag){
	obj=document.getElementById(idtag);
	if (obj){
		obj.style.visibility = "hidden";
		obj.style.display = 'none';
	}
}
function show_tag(idtag){
	obj=document.getElementById(idtag);
	if (obj){
		obj.style.visibility = "visible";
		obj.style.display = '';
	}
}
function method_change(){
	method=getmethod();
	obj=document.getElementById('postdata_row');
	if (obj){
		if (method=='GET'){
			obj.style.visibility = "hidden";
			obj.style.display = 'none';
		}else if (method=='POST'){
			obj.style.visibility = "visible";
			obj.style.display = '';
		}
	}

}
function cookies_change(){
	obj=document.getElementById('cookies_row');
	if (obj){
		if (!document.getElementById("idsendcookies").checked){
			obj.style.visibility = "hidden";
			obj.style.display = 'none';
		}else{
			obj.style.visibility = "visible";
			obj.style.display = '';
		}
	}

}

function expand_collapse(id){
	obj=document.getElementById(id);
	if (obj){
		padre=document.getElementById(id+'-p');
		if (obj.style.visibility=='visible'){
			obj.style.visibility = "hidden";
			obj.style.display = 'none';
			if (padre){padre.innerHTML='+';}
		}else{
			obj.style.visibility = "visible";
			obj.style.display = '';
			if (padre){padre.innerHTML='-';}
		}
	}
}
function addElement(idname,tag) {
	var _body = document.getElementsByTagName('body') [0];
	var newdiv = document.createElement(tag);
	newdiv.setAttribute('id',idname);
	_body.appendChild(newdiv);
}
function addElementToParent(idname,tag,idparent) {
	var _body = document.getElementById(idparent);
	var newdiv = document.createElement(tag);
	newdiv.setAttribute('id',idname);
	_body.appendChild(newdiv);
}
function removeElement(idname) {
    if (idname) {
        var el = document.getElementById(idname);
        if (el) {
            el.parentNode.removeChild(el);
        }
    }
}