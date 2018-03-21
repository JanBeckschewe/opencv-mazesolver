var forward = 0, right = 1, backward = 2, left = 3;
var fullPath = [];
var konvaFullPoints = [];
var simplePath = [];
var konvaSimplePoints = [];

var stage = new Konva.Stage({
    container: 'konva_canvas',
    width: window.innerWidth,
    height: window.innerHeight,
    draggable: true
});

var layer = new Konva.Layer({});
stage.add(layer);

var konvaFullPathLine = new Konva.Line({
    points: konvaFullPoints,
    stroke: 'red',
    strokeWidth: 10,
    closed: false
});
var konvaSimplePathLine = new Konva.Line({
    points: konvaSimplePoints,
    stroke: 'green',
    strokeWidth: 6,
    closed: false
});
var konvaFullStartPoint = new Konva.Circle({
    x: 0,
    y: 0,
    radius: 10,
    fill: 'blue'
});
var konvaFullEndPoint = new Konva.Circle({
    x: 0,
    y: 0,
    radius: 10,
    fill: 'yellow'
});
var konvaSimpleEndPoint = new Konva.Circle({
    x: 0,
    y: 0,
    radius: 10,
    fill: 'orange'
});


layer.add(konvaFullPathLine);
layer.add(konvaSimplePathLine);
layer.add(konvaFullStartPoint);
layer.add(konvaFullEndPoint);
layer.add(konvaSimpleEndPoint);

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

window.addEventListener('resize', function (ev) {
    stage.width(window.innerWidth);
    stage.height(window.innerHeight);
    draw();
});

function draw() {
    layer.offset({x: 0, y: 0});
    layer.scale({x: 1, y: 1});

    setLinePoints(fullPath, konvaFullPoints);
    setLinePoints(simplePath, konvaSimplePoints);

    konvaFullEndPoint.x(konvaFullPoints[konvaFullPoints.length - 2]);
    konvaFullEndPoint.y(konvaFullPoints[konvaFullPoints.length - 1]);

    konvaSimpleEndPoint.x(konvaSimplePoints[konvaSimplePoints.length - 2]);
    konvaSimpleEndPoint.y(konvaSimplePoints[konvaSimplePoints.length - 1]);

    var pathBoundsRect = konvaFullPathLine.getClientRect();
    layer.offset({x: pathBoundsRect.x, y: pathBoundsRect.y});

    var scalingFactor = Math.min(
        stage.width() / pathBoundsRect.width,
        stage.height() / pathBoundsRect.height);

    layer.scale({x: scalingFactor, y: scalingFactor});

    layer.draw();
}

function setLinePoints(path, konvaPoints) {
    konvaPoints.length = 0;

    var currentDir = right;
    var posPixel = {x: 0, y: 0};
    konvaPoints.push(0, 0);
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
        konvaPoints.push(posPixel.x, posPixel.y);
    });
}
