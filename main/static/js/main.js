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