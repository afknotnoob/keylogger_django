document.addEventListener("DOMContentLoaded", function () {
    // Add fade effect to messages
    setTimeout(function () {
        let messages = document.querySelector(".messages");
        if (messages) {
            messages.style.opacity = "0";
            setTimeout(() => messages.remove(), 500);
        }
    }, 3000);

    // Confirmation before clearing logs
    let clearButton = document.querySelector("#clearLogs");
    if (clearButton) {
        clearButton.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to clear all logs?")) {
                event.preventDefault();
            }
        });
    }
});
