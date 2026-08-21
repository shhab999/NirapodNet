const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.getElementById("messages");
const joinButton = document.getElementById("joinButton");

let currentUser = null;
let socket = null;

function connectWebSocket() {
    socket = new WebSocket(`ws://${window.location.host}/ws`);

    socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        addMessage(message);
    };
}

function addMessage(message) {
    const div = document.createElement("div");
    div.className = "message";
    div.textContent = `${message.sender}: ${message.content}`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    socket.send(JSON.stringify({
        sender_id: currentUser.id,
        content: text
    }));
    input.value = "";
}

async function loadMessages() {
    const response = await fetch("/messages");
    const data = await response.json();
    messages.innerHTML = "";
    data.forEach(addMessage);
}

async function joinNetwork() {
    const username = document.getElementById("usernameInput").value.trim();
    if (!username) return;

    const response = await fetch("/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username })
    });

    currentUser = await response.json();

    document.getElementById("loginBox").style.display = "none";
    document.getElementById("chatBox").style.display = "block";

    connectWebSocket();
    loadMessages();
}

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

joinButton.addEventListener("click", joinNetwork);