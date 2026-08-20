const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.getElementById("messages");

function addMessage(text) {

    const div = document.createElement("div");

    div.className = "message";
    div.textContent = "You: " + text;

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;
}

sendButton.addEventListener("click", () => {

    const text = input.value.trim();

    if (text === "") return;

    addMessage(text);

    input.value = "";
});

input.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {
        sendButton.click();
    }

});