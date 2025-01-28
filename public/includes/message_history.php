<?php
// public/includes/message_history.php - Message History Display
?>
<div id="message-history">
    <h3>Message History</h3>
    <div id="history-container">
        <!-- Messages will be dynamically inserted here -->
    </div>
</div>

<script>
function addMessageToHistory(sender, message) {
    var historyContainer = document.getElementById("history-container");
    var messageDiv = document.createElement("div");
    messageDiv.classList.add("message-entry");
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    historyContainer.appendChild(messageDiv);
}
</script>
