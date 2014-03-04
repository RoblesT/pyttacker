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
//Enviar Contenido solicitado en el codigo en el contenedor idcontenedor
function send(idcontenedor,url,method,postdata){
	var query, contenedor;
	contenedor = document.getElementById(idcontenedor);
	if (method == 'POST') {
		if (contenedor != null) {
			query = url;
			ajax=nuevoAjax();
			ajax.open("POST", query,true);
			ajax.setRequestHeader("Content-type","application/x-www-form-urlencoded");
			ajax.onreadystatechange=function() {
				if (ajax.readyState==4) {
					response = ajax.responseText;
					contenedor.innerHTML = response;
				}
			}
			ajax.send(postdata)
		}
	} else if (method == 'GET'){
		if (contenedor != null) {
			query = url;
			ajax=nuevoAjax();
			ajax.open("GET", query,true);
			ajax.onreadystatechange=function() {
				if (ajax.readyState==4) {
					response = ajax.responseText;
					contenedor.innerHTML = response;
				}
			}
			ajax.send()
		}
	}
}
function test_xfs(){
	var query, contenedor;
	contenedor = document.getElementById('results');
	url=document.getElementById('idurl').value;
	postdata="xfs="+url;
	if (contenedor != null) {
		query = url;
		ajax=nuevoAjax();
		ajax.open("POST", "/",true);
		ajax.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		contenedor.innerHTML = 'Working, please wait!';
		ajax.onreadystatechange=function() {
			if (ajax.readyState==4) {
				response = ajax.responseText;
				if (response == 'true'){
					send_xfs();
					contenedor.innerHTML = "<span style='color:red;'>XFS confirmed! The iFrame above display the working PoC</span>";
				}else if (response == 'error'){
					contenedor.innerHTML = "<span style='color:red;'>The URL seems to be invalid or the server wasn't able to reach the destination</span>";
				}else if (response != ''){
					contenedor.innerHTML = "<span style='color:green;'>The URL Provided is not vulnerable, "+response+" detected in the response headers</span>";
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
function send_xfs() {
	resetiFrame();
	poc=sendtoiFrame(document.getElementById('idurl').value);
}
function send_request() {
	
	csrf_form = document.getElementById("csrf_form");
	if (csrf_form){ 
		removeElement("csrf_form");
	}
	method=getmethod();
	if (method == 'POST'){
		addElement("csrf_form","form");
		csrf_form = document.getElementById("csrf_form");
		
		if (csrf_form){
			csrf_form.setAttribute("action", document.getElementById('idurl').value);
			csrf_form.setAttribute("method", method);
			if (document.getElementById("idtoiframe").checked){
				resetiFrame();
				csrf_form.setAttribute("target", "attack_frame");
				document.getElementById('results').innerHTML="<span style='color:red;'>CSRF Validation, check the iFrame content as a PoC if the target site is vulnerable to CSRF, if the iFrame is blank try without using the iFrame check (The site may be protected against XFS)</span>";
			}else{
				poc_window();
				csrf_form.setAttribute("target", "attack_window");
				document.getElementById('results').innerHTML="<span style='color:red;'>CSRF Validation, check the content in the new window opened, if the desired action was performed without validating any Token, then you have the PoC that confirms the target site is vulnerable to CSRF</span>";
			}		
			params = document.getElementById("iddata").value;
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
		if (document.getElementById("idtoiframe").checked){
			resetiFrame();
			sendtoiFrame(document.getElementById('idurl').value);
			document.getElementById('results').innerHTML="<span style='color:red;'>CSRF Validation, check the iFrame content as a PoC if the target site is vulnerable to CSRF, if the iFrame is blank try without using the iFrame check (The site may be protected against XFS)</span>";
		}else{
			poc_window();
			document.getElementById('results').innerHTML="<span style='color:red;'>CSRF Validation, check the content in the new window opened, if the desired action was performed without validating any Token, then you have the PoC that confirms the target site is vulnerable to CSRF</span>";
		}
	}
}
function poc_window(){
	window.open(document.getElementById('idurl').value,"attack_window","width=640,height=480");
}
function start(){
	method_change();
	poc_change()
}
function send(){
	var e = document.getElementById("cmbpoc");
	ifrm = document.getElementById("attack_frame");
	if (ifrm){removeElement("attack_frame");}
	switch( e.options[e.selectedIndex].value){
	case 'xfs':
		test_xfs();
		break;
	case 'csrf': case 'xss': case 'ptf':
		send_request();
		break;
	}
}
function poc_change(){
	hide_tag('xfs_info');
	hide_tag('xss_info');
	hide_tag('csrf_info');
	hide_tag('ptf_info');
	var e = document.getElementById("cmbpoc");    
	switch( e.options[e.selectedIndex].value){
	case 'xfs':
		show_tag('xfs_info');
		break;
	case 'csrf':
		show_tag('csrf_info');
		break;
	case 'xss':
		show_tag('xss_info');
		break;
	case 'ptf':
		show_tag('ptf_info');
		break;
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