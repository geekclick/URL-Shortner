function copyToClipboard() {
    const shortUrlElement = document.getElementById("shortUrl");
    const range = document.createRange();
    range.selectNode(shortUrlElement);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    document.execCommand("copy");
    selection.removeAllRanges();
    document.getElementById('alert').style.display='block';
    function hideAlert() {
        document.getElementById('alert').style.display = 'none';
    }
    // Set a timeout of 3 seconds to hide the alert
    const timeoutId = setTimeout(hideAlert, 3000);
}