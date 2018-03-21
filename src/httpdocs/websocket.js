var forward = 0, right = 1, backward = 2, left = 3;
var fullPath = [];
var simplePath = [];

var socket = new WebSocket('ws://' + window.location.hostname + ':8000');

socket.onopen = function (ev) {
    console.log("connected");
};

socket.onmessage = function (ev) {
    var message = JSON.parse(ev.data);
    fullPath = message.full_path;
    simplePath = message.simple_path;
    console.log(message);
    draw();
};