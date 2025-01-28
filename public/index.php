<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
// index.php - Main entry point
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Testing Tool</title>
    <link rel="stylesheet" href="styles.css">
    <script src="scripts.js" defer></script>
</head>
<body>
    
    <?php include 'includes/system_prompt.php'; ?>
    <?php include 'includes/message_history.php'; ?>
    <?php include 'includes/message_input.php'; ?>

</body>
</html>