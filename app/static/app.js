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
    sendButton.disabled = true;
    socket = new WebSocket(`ws://${window.location.host}/ws`);

    const networkStatus = document.getElementById("networkStatus");

    socket.onopen = () => {
        console.log("websocket connected");

        networkStatus.textContent = "🟢 Connected";
        networkStatus.className = "online";

        syncPendingMessages();
        updateQueueCount();

        sendButton.disabled = false;
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

        removePending(message.client_id);

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

    if (!socket || socket.readyState !== WebSocket.OPEN)
        return;

    const queue = getPendingMessages();

    queue.forEach(message => {
        socket.send(JSON.stringify(message));
    });
}

function removePending(clientId) {

    if (!clientId) return;

    const pending = document.querySelector(
        `[data-client-id="${clientId}"]`
    );

    if (pending) {
        pending.remove();
    }

    const queue = getPendingMessages().filter(
        msg => msg.client_id !== clientId
    );

    savePendingMessages(queue);

    updateQueueCount();
}

function updateQueueCount() {
    const count = getPendingMessages().length;

    document.getElementById("queueCount").textContent = `Pending: ${getPendingMessages().length}`;
}

function generateId() {
    if (window.crypto && window.crypto.randomUUID) {
        return crypto.randomUUID();
    }
    // Fallback for non-secure contexts (like HTTP network IPs)
    return 'id-' + Math.random().toString(36).substr(2, 9) + '-' + Date.now();
}

function sendMessage() {

    const text = input.value.trim();
    if (!text) return;

    const message = {
        client_id: generateId(),
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