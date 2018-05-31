const konvaSimplePoints = [];
const konvaFullPoints = [];

const stage = new Konva.Stage({
    container: 'konva_canvas',
    width: 1000,
    height: 1000,
    draggable: true
});

const layer = new Konva.Layer({});
stage.add(layer);

const konvaFullPathLine = new Konva.Line({
    points: konvaFullPoints,
    stroke: 'red',
    strokeWidth: 250,
    closed: false
});
const konvaSimplePathLine = new Konva.Line({
    points: konvaSimplePoints,
    stroke: 'green',
    strokeWidth: 150,
    closed: false
});
const konvaFullStartPoint = new Konva.Circle({
    x: 0,
    y: 0,
    radius: 300,
    fill: 'blue'
});
const konvaFullEndPoint = new Konva.Circle({
    x: 0,
    y: 0,
    radius: 300,
    fill: 'yellow'
});
const konvaSimpleEndPoint = new Konva.Circle({
    x: 0,
    y: 0,
    radius: 300,
    fill: 'orange'
});


layer.add(konvaFullPathLine);
layer.add(konvaSimplePathLine);
layer.add(konvaFullStartPoint);
layer.add(konvaFullEndPoint);
layer.add(konvaSimpleEndPoint);

function draw() {
    layer.offset({x: 0, y: 0});
    layer.scale({x: 1, y: 1});

    setLinePoints(fullPath, konvaFullPoints);
    setLinePoints(simplePath, konvaSimplePoints);

    konvaFullEndPoint.x(konvaFullPoints[konvaFullPoints.length - 2]);
    konvaFullEndPoint.y(konvaFullPoints[konvaFullPoints.length - 1]);

    konvaSimpleEndPoint.x(konvaSimplePoints[konvaSimplePoints.length - 2]);
    konvaSimpleEndPoint.y(konvaSimplePoints[konvaSimplePoints.length - 1]);

    const pathBoundsRect = konvaFullPathLine.getClientRect();

    layer.offset({x: pathBoundsRect.x, y: pathBoundsRect.y});

    const scalingFactor = Math.min(
        stage.width() / pathBoundsRect.width,
        stage.height() / pathBoundsRect.height);

    layer.scale({x: scalingFactor, y: scalingFactor});

    layer.draw();
}

function setLinePoints(path, konvaPoints) {
    konvaPoints.length = 0;

    let currentDir = right;
    const posPixel = {x: 0, y: 0};
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
