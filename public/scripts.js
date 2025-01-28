// public/scripts.js


document.addEventListener("DOMContentLoaded", function () {
    fetchPrompts();
    fetchLastPrompt();
    fetchModels();
});

// ## System prompts
function toggleSystemPrompt() {
    var promptDiv = document.getElementById("system-prompt");
    if (promptDiv.style.display === "none") {
        promptDiv.style.display = "block";
    } else {
        promptDiv.style.display = "none";
    }
}

async function fetchModels() {
    let response = await fetch("http://localhost:18086/get_models");
    let data = await response.json();
    
    let modelSelect = document.getElementById("model-select");
    modelSelect.innerHTML = ""; // Clear existing options

    data.models.forEach(model => {
        let option = document.createElement("option");
        option.value = model;
        option.textContent = model.replace("-", " ").toUpperCase(); // Format nicely
        modelSelect.appendChild(option);
    });
}

async function fetchPrompts() {
    let response = await fetch("http://localhost:18086/get_prompts");
    let data = await response.json();
    
    let promptSelect = document.getElementById("prompt-select");
    promptSelect.innerHTML = ""; // Clear existing options

    data.forEach(prompt => {
        let option = document.createElement("option");
        option.value = prompt;
        option.textContent = prompt.replace(/_/g, " "); // ✅ Convert underscores to spaces for display
        promptSelect.appendChild(option);
    });
}

async function fetchLastPrompt() {
    let response = await fetch("http://localhost:18086/get_last_prompt");
    let data = await response.json();
    let lastPrompt = data.last_prompt;

    if (lastPrompt) {
        document.getElementById("prompt-select").value = lastPrompt;
        loadPrompt();
    }
}

async function loadPrompt() {
    let promptSelect = document.getElementById("prompt-select");
    let selectedPrompt = promptSelect.value.trim();
    
    if (!selectedPrompt) return;

    let encodedPrompt = encodeURIComponent(selectedPrompt);

    let response = await fetch(`http://localhost:18086/get_prompt?name=${encodedPrompt}`);
    
    if (response.ok) {
        let data = await response.json();
        document.getElementById("system-prompt").value = data.prompt;

        // Populate version dropdown
        let versionSelect = document.getElementById("version-select");
        versionSelect.innerHTML = ""; // Clear existing options

        // Add "Latest" as the first option
        let latestOption = document.createElement("option");
        latestOption.value = "latest";
        latestOption.textContent = "Latest";
        versionSelect.appendChild(latestOption);

        data.versions.forEach(version => {
            let option = document.createElement("option");
            option.value = version.version;
            option.textContent = `Version ${version.version}`;
            versionSelect.appendChild(option);
        });

        // Set "Latest" as the default selection
        versionSelect.value = "latest";
    } else {
        console.error("Failed to load system prompt.");
    }
}

async function savePrompt() {
    let promptName = document.getElementById("prompt-name").value.trim();
    let promptText = document.getElementById("system-prompt").value.trim();
    let saveMessage = document.getElementById("save-message");

    // If the new prompt name is empty, use the currently selected prompt
    if (!promptName) {
        promptName = document.getElementById("prompt-select").value;
    }

    if (!promptName || !promptText) {
        saveMessage.textContent = "Please enter a name and prompt.";
        return;
    }

    let response = await fetch("http://localhost:18086/save_prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: promptName, prompt: promptText })
    });

    let result = await response.json();
    saveMessage.textContent = result.message;
    fetchPrompts();
}


async function loadPromptVersion() {
    let promptName = document.getElementById("prompt-select").value;
    let version = document.getElementById("version-select").value;
    
    if (!promptName || !version) return;

    let encodedPrompt = encodeURIComponent(promptName);
    
    let response = await fetch(`http://localhost:18086/get_prompt?name=${encodedPrompt}&version=${version}`);
    let data = await response.json();

    document.getElementById("system-prompt").value = data.prompt;
}

// ## Chat History
document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.querySelector("#message-input-container button");
    if (sendButton) {
        sendButton.addEventListener("click", sendMessage);
    }
});

async function sendMessage() {
    var messageBox = document.getElementById("user-message");
    var message = messageBox.value.trim();
    var modelSelect = document.getElementById("model-select"); // Get selected model
    var selectedModel = modelSelect.value;

    if (message !== "") {
        addMessageToHistory("You", message);
        messageBox.value = "";

        // Collect chat history
        var messages = document.querySelectorAll("#history-container .message-entry");
        var history = [];
        messages.forEach(msg => {
            history.push(msg.innerText);
        });

        // Send message history and model to the Python server
        let response = await fetch("http://localhost:18086/send_message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ history: history, model: selectedModel })
        });

        let data = await response.json();
        addMessageToHistory("AI Agent", data.response);
    }
}

function addMessageToHistory(sender, message) {
    var historyContainer = document.getElementById("history-container");
    if (historyContainer) {
        var messageEntry = document.createElement("div");
        messageEntry.classList.add("message-entry");
        messageEntry.innerHTML = `<strong>${sender}:</strong> ${message}`;
        historyContainer.appendChild(messageEntry);
    }
}


