// script.js

document.getElementById('send-btn').addEventListener('click', function () {
    let userMessage = document.getElementById('chat-input').value;
    let csrfToken = document.getElementById('csrf_token').value;
    if (userMessage.trim() !== "") {
        $.ajax({
            url: "{% url 'get_input/' %}",  // URL should match the path you define in urls.py
            type: "POST",
            data: {
                message: userMessage,
                csrfmiddlewaretoken: csrfToken  // For CSRF protection
            },
            success: function(response) {
                // Append user's message to chat-box
                document.getElementById("chat-box").innerHTML += "<p><b>You:</b> " + userMessage + "</p>";
                
                // Append bot's response to chat-box
                document.getElementById("chat-box").innerHTML += "<p><b>Bot:</b> " + response.response + "</p>";
            },
            error: function() {
                alert("An error occurred");
            }
        });
        document.getElementById('chat-input').value = ""; // Clears the input field
        stopTypingAnimation();  // Stop the typing animation
    }
});
