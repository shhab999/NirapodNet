const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.getElementById("messages");
const joinButton = document.getElementById("joinButton");

let currentUser = null;
let socket = null;
let reconnectTimer = null;

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

        sendButton.disabled = true;

        reconnect();
    };

    socket.onerror = () => {
        networkStatus.textContent = "🔴 Connection Error";
        networkStatus.className = "offline";
    };

    socket.onmessage = (event) => {

        const data = JSON.parse(event.data);

        if (data.type === "ack") {

            removePending(data.client_id);
            return;
        }

        if (data.type === "message") {

            addMessage(data);
            return;
        }

        if (data.type === "error") {

            console.error("Server error:", data.error);

            if (data.client_id) {
                showPendingMessage({
                    client_id: data.client_id,
                    sender: currentUser.username,
                    content: data.error
                });
            }
        }
    };
}

function reconnect() {

    if (reconnectTimer) {
        return;
    }

    reconnectTimer = setTimeout(() => {

        reconnectTimer = null;

        if (!socket || socket.readyState === WebSocket.CLOSED) {
            connectWebSocket();
        }
    }, 3000);
}

function addMessage(message) {
    if (message.id && displayedMessages.has(message.id)) {
        return;
    }

    if (message.id) {
        displayedMessages.add(message.id);
    }

    const pending = document.querySelector(
        `[data-client-id="${message.client_id}"]`
    );

    if (pending) {
        pending.remove();
    }

    const div = document.createElement("div");

    div.className = "message";

    if (message.sender_id === currentUser.id) {
        div.classList.add("mine");
    } else {
        div.classList.add("other");
    }

    const sender = document.createElement("strong");
    sender.textContent = message.sender;

    const content = document.createElement("div");
    content.textContent = message.content;

    const status = document.createElement("div");
    status.className = "delivery";
    status.textContent = "Delivered";

    div.appendChild(sender);
    div.appendChild(content);
    div.appendChild(status);

    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function showPendingMessage(message) {
    const existing = document.querySelector(
        `[data-client-id="${message.client_id}"]`
    );

    if (existing) {
        return;
    }

    const div = document.createElement("div");

    div.className = "message pending";
    div.dataset.clientId = message.client_id;

    const sender = document.createElement("strong");
    sender.textContent = message.sender;

    const content = document.createElement("div");
    content.textContent = message.content;

    const status = document.createElement("div");
    status.className = "delivery";
    status.textContent = "Pending";

    div.appendChild(sender);
    div.appendChild(content);
    div.appendChild(status);

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;
}

function restorePendingMessages() {

    const queue = getPendingMessages();

    queue.forEach(message => {

        showPendingMessage(message);

    });

    updateQueueCount();
}

async function loadMessages() {

    try {

        const response = await fetch("/messages");

        if (!response.ok) {
            throw new Error("Failed to load messages");
        }

        const data = await response.json();

        messages.innerHTML = "";

        data.forEach(addMessage);

        restorePendingMessages();

    } catch (error) {

        console.error("Message loading failed:", error);

    }
}

function trySendPendingMessages() {

    if (!socket || socket.readyState !== WebSocket.OPEN) {
        return;
    }

    const queue = getPendingMessages();

    for (const message of queue) {

        socket.send(JSON.stringify(message));

    }
}

function syncPendingMessages() {
    trySendPendingMessages();
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

    document.getElementById("queueCount").textContent =
        `Pending: ${count}`;
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

    const queue = getPendingMessages();
    queue.push(message);
    savePendingMessages(queue);
    showPendingMessage(message);
    updateQueueCount();

    input.value = "";
    trySendPendingMessages();

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