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
    var fileInput = document.getElementById('file');   
    
    fileInput.click();
    document.getElementById('fileInputName').textContent = fileInput.files[0].name;
}