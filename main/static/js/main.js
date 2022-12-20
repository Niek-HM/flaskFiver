function selectFile() { // NOTE click the file input when the button is pressed 
    $(document.getElementById('file')).click();
};

$(document).ready(function() { // NOTE Change classes when a file is selected
    $(document.getElementById('file')).change(function(e) {
        document.getElementById('fileInputName').textContent = document.getElementById('file').files[0].name;
        document.getElementById('fileButton').classList.remove('btn-secondary');
        document.getElementById('fileButton').classList.add('btn-primary');
    });
});

function changeImage(element) { // NOTE Change first image when pressed
    var main_prodcut_image = document.getElementById('main_product_image');
    main_prodcut_image.src = element.src;
}