const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.getElementById("messages");
const joinButton = document.getElementById("joinButton");

let currentUser = null;
let socket = null;

const displayedMessages = new Set();

const QUEUE_KEY = "nirapodnet_pending_messages";

function getPendingMessages() {
    return JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
}

function savePendingMessages(queue) {
    localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
}

function connectWebSocket() {
    socket = new WebSocket(`ws://${window.location.host}/ws`);

    const networkStatus = document.getElementById("networkStatus");

    socket.onopen = () => {
        networkStatus.textContent = "🟢 Connected";
        networkStatus.className = "online";

        syncPendingMessages();
    };

    socket.onclose = () => {
        networkStatus.textContent = "🔴 Offline";
        networkStatus.className = "offline";

        reconnect();
    };

    socket.onerror = () => {
        networkStatus.textContent = "🔴 Connection Error";
        networkStatus.className = "offline";
    };

    socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.client_id) {
            removePending(message.client_id);
        }
        addMessage(message);
    };
}

function reconnect() {
    setTimeout(() => {
        if (!socket || socket.readyState === WebSocket.CLOSED) {
            connectWebSocket();
        }
    }, 3000);
}

function addMessage(message) {
    if (message.id && displayedMessages.has(message.id)) return;
    if (message.id) displayedMessages.add(message.id);

    const div = document.createElement("div");
    div.className = "message";

    if (message.sender_id === currentUser.id) {
        div.classList.add("mine");
    } else {
        div.classList.add("other");
    }

    div.innerHTML = `
        <strong>${message.sender}</strong><br>
        ${message.content}
        <div class="delivery">Delivered</div>
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function showPendingMessage(message) {
    const div = document.createElement("div");
    div.className = "message pending";
    div.dataset.clientId = message.client_id;
    div.innerHTML = `
        <strong>${message.sender}</strong><br>
        ${message.content}
        <div class="delivery">Pending</div>
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function syncPendingMessages() {
    const queue = getPendingMessages();

    if (!socket || socket.readyState !== WebSocket.OPEN) return;
    if (queue.length === 0) return;

    queue.forEach(message => {
        socket.send(JSON.stringify(message));
    });

    // Queue is cleared only after each message is confirmed in removePending()
}

function removePending(clientId) {
    let queue = getPendingMessages();
    queue = queue.filter(m => m.client_id !== clientId);
    savePendingMessages(queue);

    updateQueueCount();

    const pendingDiv = messages.querySelector(`.pending[data-client-id="${clientId}"]`);
    if (pendingDiv) {
        pendingDiv.remove();
    }
}

function updateQueueCount() {
    document.getElementById("queueCount").textContent = `Pending: ${getPendingMessages().length}`;
}

function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    const message = {
        client_id: crypto.randomUUID(),
        sender_id: currentUser.id,
        sender: currentUser.username,
        content: text,
        created_at: new Date().toISOString()
    };

    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    } else {
        const queue = getPendingMessages();
        queue.push(message);
        savePendingMessages(queue);

        showPendingMessage(message);
        updateQueueCount();
    }

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

    document.getElementById("userLabel").textContent = `Logged in as ${currentUser.username}`;

    document.getElementById("loginBox").style.display = "none";
    document.getElementById("chatBox").style.display = "block";

    connectWebSocket();
    loadMessages();
    updateQueueCount();
}

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

joinButton.addEventListener("click", joinNetwork);