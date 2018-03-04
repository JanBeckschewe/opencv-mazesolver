var forward = 0, right = 1, backward = 2, left = 3;
var path = [];
var points = [];

var stage = new Konva.Stage({
    container: 'konva_canvas',
    width: window.innerWidth,
    height: window.innerHeight,
    draggable: true
});

var layer = new Konva.Layer({});
stage.add(layer);

var path_line = new Konva.Line({
    points: points,
    stroke: 'red',
    strokeWidth: 10,
    closed: false
});
layer.add(path_line);

var socket = new WebSocket('ws://' + window.location.hostname + ':8000');
socket.onopen = function (ev) {
    console.log("connected");
};
socket.onmessage = function (ev) {
    console.log("received");
    path = JSON.parse(ev.data);
    console.log(path);
    draw();
    socket.send("k");
};

window.addEventListener('resize', function (ev) {
    stage.width(window.innerWidth);
    stage.height(window.innerHeight);
    draw();
});

function draw() {
    var currentDir = right;
    var posPixel = {x: 0, y: 0};

    path.forEach(function (element) {
        currentDir = (currentDir + element[0]) % 4;

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
    });

    var pathBoundsRect = path_line.getClientRect();
    console.log(pathBoundsRect);
    console.log("w,h", stage.width(), stage.height());
    path_line.offsetX(pathBoundsRect.x);
    path_line.offsetY(pathBoundsRect.y);

    var scalingFactor = Math.min(stage.width() / pathBoundsRect.width, stage.height() / pathBoundsRect.height);
    console.log("scalingFactor", scalingFactor);

    path_line.scale({x: scalingFactor, y: scalingFactor});

    layer.draw();
}