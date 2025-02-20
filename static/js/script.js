document.addEventListener("DOMContentLoaded", function () {
    const socket = io();
    const messageInput = document.getElementById("messageInput"); // Ensure this ID exists in your HTML
    const typingIndicator = document.getElementById("typingIndicator"); // Add this in your HTML

    let typing = false;
    let timeout;

    function timeoutFunction() {
        typing = false;
        socket.emit("typing", { room: roomCode, typing: false });
    }

    messageInput.addEventListener("keyup", function () {
        if (!typing) {
            typing = true;
            socket.emit("typing", { room: roomCode, typing: true });
        }
        clearTimeout(timeout);
        timeout = setTimeout(timeoutFunction, 2000);
    });

    socket.on("user_typing", function (data) {
        if (data.typing) {
            typingIndicator.innerText = `${data.username} is typing...`;
        } else {
            typingIndicator.innerText = "";
        }
    });
});