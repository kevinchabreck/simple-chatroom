function createCanvas(parent, width, height){
	var canvas = {};
	canvas.node = document.createElement('canvas');
	canvas.context = canvas.node.getContext('2d');
	canvas.node.width = 500;
	canvas.node.height = 500;
	parent.appendChild(canvas.node);
	return canvas;
}

function createResetButton(parent){
	var button = {};
	button.node = document.createElement('input');
	button.node.type = 'submit';
	button.node.id = 'reset';
	button.node.value = "Reset!";
	parent.appendChild(button.node)
	return button;
}

function createInputBox(parent){
	var textBox = {};
	textBox.node = document.createElement('textarea');
	textBox.node.rows = 5;
	textBox.node.cols = 32;
	textBox.node.maxlength = 100;
	textBox.node.placeholder = 'say something!'
	wrap = "hard";
	textBox.node.id = 'inputBox';
	parent.appendChild(textBox.node);
	return textBox;
}

function init(container, width, height, fillColor) {

	var canvas = createCanvas(container, width, height);
	var ctx = canvas.context;
	var resetButton = createResetButton(document.getElementById('buttonSpace'));
	var inputBox = createInputBox(document.getElementById('textEntrySpace'));
	var username = null;
	var oldX = null;
	var oldY = null;
	
	ctx.draw = function(oX, oY, nX, nY, width, fillColor) {
		this.strokeStyle = fillColor;
		this.beginPath();
		this.moveTo(oX, oY);
		this.lineTo(nX, nY);
		this.closePath();
		this.lineWidth = width;
		this.stroke();
		oldX = nX;
		oldY = nY;
	};
	
	ctx.clear = function() {
		ctx.fillStyle = "#ddd";
		ctx.fillRect(0, 0, width, height);
	};

	ctx.clear();

	canvas.node.onmousemove = function(e) {
		if(canvas.isDrawing){
			var newX = e.pageX - this.offsetLeft;
			var newY = e.pageY - this.offsetTop;
			var width = 5;
			var fillColor = '#ff0000';
			ws.send('PAINT:'+oldX+' '+oldY+' '+newX+' '+newY+' '+width+' '+fillColor);
		}
	};

	canvas.node.onmousedown = function(e) { 
		oldX = e.pageX - this.offsetLeft;
		oldY = e.pageY - this.offsetTop;
		canvas.isDrawing = true; 
	};
	
	canvas.node.onmouseup = function(e) { canvas.isDrawing = false; };
	resetButton.node.onclick = function(e) { ws.send('RESET:'); };
	inputBox.node.onclick = function(e){ inputBox.node.placeholder = ''; };
	inputBox.node.onkeypress = function(e) {
		if (e.keyCode == 13)
			sendText();
	};

	function sendText(e){
		ws.send('CHAT:' + inputBox.node.value);
		inputBox.node.value = '';
	}

	ws = new WebSocket("ws://localhost:15013/");
	ws.onopen = function() { 
		username = window.prompt("Enter your username");
		ws.send('USERNAME:' + username);
	};
	ws.onclose = function() { alert('server shut down'); };

	// possible message headers: 
	// CHAT, PAINT, RESET, ACCEPTED, DENIED, INFO, PAINTBUFFER, USERS
	ws.onmessage = function(e) {
		var params = e.data.split(':');
		var header = params[0];
		if (header == 'PAINT'){
			params = params[1].split(' ')
			ctx.draw(params[0], params[1], params[2], params[3], params[4], params[5]);
		}
		else if((header == 'CHAT')||(header == 'INFO')){
			var msg = e.data.replace(header+':','',1);
			if (header == 'INFO')
				msg = '<i>'+msg+'</i>';
			else if (header == 'CHAT')
				msg = '<b>' + msg.replace(':','</b>:',1);
			var messageSpace = document.getElementById("messagesSpace");
			messageSpace.innerHTML += msg + '</br></br>';
			messageSpace.scrollTop = messageSpace.scrollHeight;
			messageSpace.focus();
		}
		else if (header == 'RESET'){ ctx.clear(); }
		else if (header == 'ACCEPTED'){
			document.title = username + ' - Paint Chat'
			ws.send('GETPAINTBUFFER:');	
		}
		else if (header == 'DENIED'){
			var reason = params[1];
			username = window.prompt("Denied!\nReason: "+reason+"\nEnter new username");
			ws.send('USERNAME:' + username);
		}
		else if (header == 'PAINTBUFFER'){
			var paintbuffer = JSON.parse(params[1]);
			for(var i in paintbuffer){
				i = paintbuffer[i].split(' ');
				ctx.draw(i[0], i[1], i[2], i[3], i[4], i[5]);
			}
		}
		else if (header == 'USERS'){
			var userlist = JSON.parse(params[1]);
			var userlistSpace = document.getElementById("userlistSpace");
			ul = '</br><b>USERS</b></br>';
			ul += '<i>'+userlist.length+' user(s) online</i><hr>';
			for(var i in userlist){
				ul += userlist[i] + '</br>';
			}
			userlistSpace.innerHTML = ul;
		}
	};
}

window.onload = function(){
	var container = document.getElementById('canvasSpace');
	init(container, 500, 500, '#ddd');
}