// ==========================================
// SHOPSPHERE JAVASCRIPT
// ==========================================
// AUTO HIDE FLASH MESSAGES
setTimeout(function () {
    let alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
        let bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);
// CONFIRM DELETE
document.addEventListener("DOMContentLoaded", function () {
    let deleteButtons = document.querySelectorAll(".btn-danger");
    deleteButtons.forEach(function (button) {
        button.addEventListener("click", function (e) {
            if (
                button.innerText.includes("Delete")
            ) {
                let confirmDelete = confirm(
                    "Are you sure you want to delete this product?"
                );
                if (!confirmDelete) {
                    e.preventDefault();
                }
            }
        });
    });
});
// IMAGE FALLBACK
document.addEventListener("DOMContentLoaded", function () {
    let images = document.querySelectorAll("img");
    images.forEach(function (img) {
        img.onerror = function () {
            this.src =
                "https://via.placeholder.com/400x300?text=No+Image";
        };
    });
});
// PRODUCT CARD HOVER EFFECT
document.addEventListener("DOMContentLoaded", function () {
    let cards = document.querySelectorAll(".product-card");
    cards.forEach(function (card) {
        card.addEventListener("mouseenter", function () {
            card.style.transition =
                "all 0.3s ease";
        });
    });
});
// SCROLL TO TOP BUTTON
window.addEventListener("scroll", function () {
    let topBtn =
        document.getElementById("scrollTopBtn");
    if (topBtn) {
        if (window.scrollY > 300) {
            topBtn.style.display = "block";
        } else {
            topBtn.style.display = "none";
        }
    }
});
// SMOOTH SCROLL
document.addEventListener("DOMContentLoaded", function () {
    document
        .querySelectorAll('a[href^="#"]')
        .forEach(anchor => {
            anchor.addEventListener("click", function (e) {
                e.preventDefault();
                const target =
                    document.querySelector(
                        this.getAttribute("href")
                    );
                if (target) {
                    target.scrollIntoView({
                        behavior: "smooth"
                    });
                }
            });
        });
});
// PAGE LOADED MESSAGE
console.log(
    "ShopSphere Marketplace Loaded Successfully"
);