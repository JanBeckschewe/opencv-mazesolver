var path = [];

var forward = 0, right = 1, backward = 2, left = 3;


var stage = new Konva.Stage({
    container: 'container',
    width: 1000,
    height: 700
});
var layer = new Konva.Layer();
var rect = new Konva.Rect({
    x: 50,
    y: 50,
    width: 100,
    height: 50,
    fill: 'green',
    stroke: 'black',
    strokeWidth: 4
});

layer.add(rect);
stage.add(layer);

function draw() {
    var currentDir = 1;
    var points = [];
    var posPixel = {x: 0, y: 0};

    path.forEach(function (element) {
        currentDir = (currentDir + element[0]) % 4;
        console.log(currentDir);

        if (currentDir === left) {
            posPixel.x -= element[1]
        }
        else if (currentDir === forward) {
            posPixel.y -= element[1];
        }
        else if (currentDir === right) {
            posPixel.x += element[1];
        }
        else if (currentDir === backward) {
            posPixel.y += element[1];
        }
        points.push(posPixel.x, posPixel.y);

        rect.height = 200;
    });
    console.log(points);

    var konva_line = new Konva.Line({
        points: points,
        stroke: 'red',
        strokeWidth: 10
    });

    layer.add(konva_line);
    layer.draw();
}

var socket = new WebSocket('ws://' + window.location.hostname + ':8000');
socket.onopen = function (ev) {
    console.log("connected");
};
socket.onmessage = function (ev) {
    console.log("received");
    path = JSON.parse(ev.data);
    draw();
    socket.send("k");
};