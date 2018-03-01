var path = [];

var stage = new Konva.Stage({
    container: 'container',
    width: 500,
    height: 300
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

var konva_line = new Konva.Line({
    points: [],
    stroke: 'green',
    strokeWidth: 10,
});

layer.add(rect);
layer.add(konva_line);
stage.add(layer);

function draw() {
    var currentDir = 1;
    path.forEach(element = > {
        console.log(element);
    currentDir = element[1];

    var posPixel = new Point(0, 0);
    if (currentDir == 0) {
        posPixel.x -= element[1]
    }
    else if (currentDir == 1) {
        posPixel.y -= element[1];
    }
    else if (currentDir == 2) {
        posPixel.x += element[1];
    }
    else if (currentDir == 3) {
        posPixel.y += element[1];
    }
    konva_line.points.add(posPixel.x, posPixel.y);
})
    ;
}

var socket = new WebSocket('ws://' + window.location.hostname + ':8000');
socket.onopen = function (ev) {
    console.log("connected");
};
socket.onmessage = function (ev) {
    console.log("received");
    path = JSON.parse(ev.data);
    setTimeout(1000);
    draw();
    socket.send("k");
};