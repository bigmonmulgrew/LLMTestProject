<?php
// public/includes/system_prompt.php - System Prompt Management
?>

<div id="system-prompt-container">
    <div id="system-prompt-controls">
        <label for="prompt-select">Select System Prompt:</label>
        <select id="prompt-select" onchange="loadPrompt()">
            <option value="">-- Select a Prompt --</option>
        </select>

        <label for="version-select">Version:</label>
        <select id="version-select" onchange="loadPromptVersion()">
            <option value="latest">Latest</option>
        </select>

        <label for="model-select">Select Model:</label>
        <select id="model-select">
            <option value="">Loading models...</option>
        </select>

        <label for="prompt-name">New Prompt Name:</label>
        <input type="text" id="prompt-name" placeholder="Enter new prompt name">
    </div>
    <div id="system-prompt-input-box">
        <label for="system-prompt">System Prompt:</label>
        <textarea id="system-prompt" rows="4" placeholder="Enter system prompt..."></textarea>

        <button onclick="savePrompt()">Save Prompt</button>
        <span id="save-message" style="color: green; margin-left: 10px;"></span>
    </div>
</div>
