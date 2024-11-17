function setupControlPanel() {
    const toggleControlPanel = document.getElementById('toggle-control-panel');
    const controlPanel = document.getElementById('control-panel');
    const fontSizeInput = document.getElementById('font-size');
    const textColorInput = document.getElementById('text-color');
    const bgColorInput = document.getElementById('bg-color');

    toggleControlPanel.addEventListener('change', function() {
        controlPanel.style.display = this.checked ? 'block' : 'none';
    });

    fontSizeInput.addEventListener('input', function() {
        document.body.getElementsByTagName('main')[0].style.fontSize = this.value + 'px';
    });

    textColorInput.addEventListener('input', function() {
        document.body.getElementsByTagName('main')[0].style.color = this.value;
    });

    bgColorInput.addEventListener('input', function() {
        document.body.style.backgroundColor = this.value;
    });
}