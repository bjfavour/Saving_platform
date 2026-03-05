// ========================================
// STEP 1: When page loads, check subscription
// ========================================

window.addEventListener("load", function () {
    checkSubscriptionStatus();
});


// ========================================
// STEP 2: Ask backend if subscription is valid
// ========================================

function checkSubscriptionStatus() {

    const token = localStorage.getItem("access");

    // Try calling a protected API
    fetch("http://127.0.0.1:8000/api/savings/payments/", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(response => {

        // If backend says 403 → subscription expired
        if (response.status === 403) {

            freezeDashboard();
            showSubscriptionModal();
        }
    })
    .catch(error => {
        console.log("Error checking subscription:", error);
    });
}


// ========================================
// STEP 3: Freeze dashboard (make it unclickable)
// ========================================

function freezeDashboard() {

    const main = document.getElementById("mainContent");

    main.style.pointerEvents = "none";   // disable clicks
    main.style.opacity = "0.4";          // fade screen

    document.getElementById("subscriptionStatus").innerText =
        "Status: Expired";
}


// ========================================
// STEP 4: Show popup
// ========================================

function showSubscriptionModal() {

    document.getElementById("subscriptionModal")
        .classList.add("active");
}


// ========================================
// STEP 5: Activate subscription
// ========================================

function activateSubscription() {

    const pin = document.getElementById("subscriptionPin").value;

    if (!pin) {
        document.getElementById("subscriptionMessage").innerHTML =
            "<span style='color:red;'>Please enter PIN</span>";
        return;
    }

    fetch("http://127.0.0.1:8000/api/subscription/activate/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            pin_code: pin
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.message) {

            document.getElementById("subscriptionMessage").innerHTML =
                "<span style='color:green;'>Subscription Activated!</span>";

            setTimeout(() => {
                location.reload();  // reload dashboard
            }, 1500);

        } else {

            document.getElementById("subscriptionMessage").innerHTML =
                "<span style='color:red;'>Invalid or Used PIN</span>";
        }

    })
    .catch(error => {
        console.log("Activation error:", error);
    });
}