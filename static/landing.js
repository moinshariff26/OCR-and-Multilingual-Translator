// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Get references to the buttons
    const getStartedBtn = document.getElementById("get-started-btn");
    const tryToolBtn = document.getElementById("try-tool-btn");

    // Add click event listeners
    if (getStartedBtn) {
        getStartedBtn.addEventListener("click", () => {
            // Navigate to the tool page
            window.location.href = "/tool";
        });
    }

    if (tryToolBtn) {
        tryToolBtn.addEventListener("click", () => {
            // Navigate to the tool page
            window.location.href = "/tool";
        });
    }
});
