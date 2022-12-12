function showPopup() {
    var input = window.prompt('Verifecation number. (You should have received an email)', '123456');

    if (input.length == 6) { // and only contains numbers
        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://10.200.34.179:5000/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({input: input}));
    }
};

function selectFile() {
    $(document.getElementById('file')).click();
};

$(document).ready(function() {
    $(document.getElementById('file')).change(function(e) {
        document.getElementById('fileInputName').textContent = document.getElementById('file').files[0].name;
        document.getElementById('fileButton').classList.remove('btn-secondary');
        document.getElementById('fileButton').classList.add('btn-primary');
    });
});

function changeImage(element) {
    var main_prodcut_image = document.getElementById('main_product_image');
    main_prodcut_image.src = element.src;
}