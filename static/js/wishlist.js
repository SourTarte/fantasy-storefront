// New: send POST to add_to_wishlist URL, show Bootstrap modal on success.
document.addEventListener("DOMContentLoaded", () => {
    // helper to get CSRF token from cookie (Django default)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie("csrftoken");

    // Utility to show the Bootstrap alert with a message
    function showWishlistAlert(message, timeoutMs = 3000) {
        const alertEl = document.getElementById("wishlistAlert");
        const msgEl = document.getElementById("wishlistAlertMessage");
        if (!alertEl || !msgEl) {
            alert(message || "Saved To Wishlist");
            return;
        }
        msgEl.textContent = message || "Saved To Wishlist";
        alertEl.classList.remove("d-none");
        // trigger fade-in
        setTimeout(() => alertEl.classList.add("show"), 10);
        // auto-hide after timeout
        if (timeoutMs > 0) {
            setTimeout(() => {
                alertEl.classList.remove("show");
                // give fade time before hiding completely
                setTimeout(() => alertEl.classList.add("d-none"), 200);
            }, timeoutMs);
        }
    }

    // Attach handlers to wishlist buttons
    document.querySelectorAll(".btn-add-wishlist").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const url = btn.getAttribute("data-url");
            if (!url) return;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({}),
            })
                .then((r) => r.json())
                .then((data) => {
                    showWishlistAlert(data.message || "Saved To Wishlist");
                })
                .catch(() => {
                    showWishlistAlert("Could not save to wishlist. Please try again.", 4000);
                });
        });
    });
});