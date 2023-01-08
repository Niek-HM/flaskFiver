function selectFile() { // NOTE click the file input when the button is pressed 
    $(document.getElementById('file')).click();
};

$(document).ready(function() { // NOTE Change classes when a file is selected
    $(document.getElementById('file')).change(function(e) {
        input = document.getElementById('fileInputName');
        input.textContent = document.getElementById('file').files[0].name;
        
        button = document.getElementById('fileButton');
        button.classList.remove('btn-secondary');
        button.classList.add('btn-primary');
        
        button.style.removeProperty('display');

        const [file] = document.getElementById('file').files;
        if (file) {
            document.getElementById('fileImg').src = URL.createObjectURL(file);
        }
    });
});

function changeImage(element) { // NOTE Change first image when pressed
    var main_prodcut_image = document.getElementById('main_product_image');
    main_prodcut_image.src = element.src;
}

function search() {
    var input = document.getElementById('searchInput').value.split(':');
    switch(input[0]) {
        case 'user': var win = window.open('http://niekhm.pythonanywhere.com/user/'+input.slice(1)); break;
        case 'product': var win = window.open('http://niekhm.pythonanywhere.com/search/' + input.slice(1)); break;
        case '': var win = window.open('http://niekhm.pythonanywhere.com/search/*/'); break;
        default: var win = window.open('http://niekhm.pythonanywhere.com/search/' + input.toString().replace(',', ''))
    }

    win.focus();
}