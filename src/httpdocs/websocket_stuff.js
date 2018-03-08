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
layer.add(konvaFullPathLine);
layer.add(konvaSimplePathLine);

var socket = new WebSocket('ws://' + window.location.hostname + ':8000');
socket.onopen = function (ev) {
    console.log("connected");
};

var obj;
socket.onmessage = function (ev) {
    obj = JSON.parse(ev.data);
    fullPath = obj.full_path;
    simplePath = obj.simple_path;
    console.log(obj);
    draw();
};

window.addEventListener('resize', function (ev) {
    stage.width(window.innerWidth);
    stage.height(window.innerHeight);
    draw();
});

function draw() {
    setLinePoints(fullPath, konvaFullPoints, konvaFullPathLine);
    setLinePoints(simplePath, konvaSimplePoints, konvaSimplePathLine);

    var pathBoundsRect = konvaFullPathLine.getClientRect();
    konvaFullPathLine.offsetX(pathBoundsRect.x);
    konvaFullPathLine.offsetY(pathBoundsRect.y);
    konvaSimplePathLine.offsetX(pathBoundsRect.x);
    konvaSimplePathLine.offsetY(pathBoundsRect.y);


    var scalingFactor = Math.min(stage.width() / pathBoundsRect.width, stage.height() / pathBoundsRect.height);

    konvaFullPathLine.scale({x: scalingFactor, y: scalingFactor});
    konvaSimplePathLine.scale({x: scalingFactor, y: scalingFactor});

    layer.draw();
}

function setLinePoints(path, konvaPoints, konvaLine) {
    konvaPoints.length = 0;
    konvaLine.scale({x: 1, y: 1});
    konvaLine.offsetX(0);
    konvaLine.offsetY(0);

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
        konvaPoints.push(posPixel.x, posPixel.y);
    });
}
