function fitStageIntoParentContainer() {
    const container = document.querySelector('#stage-parent');

    const containerWidth = container.offsetWidth;
    const scale = containerWidth / 1000;

    stage.width(1000 * scale);
    stage.height(1000 * scale);
    stage.scale({x: scale, y: scale});
    stage.draw();
}

fitStageIntoParentContainer();

window.addEventListener('resize', fitStageIntoParentContainer);