let forward = 0, right = 1, backward = 2, left = 3;
let fullPath = [];
let simplePath = [];
let socket;

function connect() {
    socket = new WebSocket('wss://' + window.location.hostname + '/ws');

    socket.onopen = function () {
        console.log("connected");
    };

    socket.onmessage = function (ev) {
        const message = JSON.parse(ev.data);
        fullPath = message.full_path;
        simplePath = message.simple_path;
        console.log(message);
        draw();
    };

    socket.onclose = function (ev) {
        console.log("disconnected:", ev.reason);
        setTimeout(connect, 1000);
    };

    socket.onerror = function (ev) {
        console.log("error: " + ev.message);
        socket.close();
    };
}

connect();
