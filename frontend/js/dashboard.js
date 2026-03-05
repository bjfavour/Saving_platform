// ===============================
// PROTECT DASHBOARD
// ===============================

const token = localStorage.getItem("access");

if (!token) {
    window.location.href = "login.html";
}


// ===============================
// FETCH DASHBOARD SUMMARY
// ===============================

fetch("http://127.0.0.1:8000/api/savings/summary/", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
})
.then(async response => {

    // handle subscription expiration
    if (response.status === 403) {

        const data = await response.json();

        if (data.detail === "Subscription expired") {

            alert("Your subscription has expired. Please renew to continue.");

            window.location.href = "subscription.html";

            return null;
        }
    }

    return response.json();
})
.then(data => {

    if (!data) return;

    // ===============================
    // UPDATE SUMMARY CARDS
    // ===============================

    document.getElementById("totalPayments").innerText =
        "₦ " + data.total_payments;

    document.getElementById("totalFees").innerText =
        "₦ " + data.total_fees;

    document.getElementById("totalCashouts").innerText =
        "₦ " + data.total_cashouts;

    document.getElementById("availableBalance").innerText =
        "₦ " + data.available_balance;


    // ===============================
    // UPDATE RECENT TRANSACTIONS
    // ===============================

    const tableBody = document.getElementById("recentTransactions");

    tableBody.innerHTML = "";

    data.recent_transactions.forEach(tx => {

        const row = `
            <tr>
                <td>${tx.date}</td>
                <td>${tx.type}</td>
                <td>₦ ${tx.amount}</td>
                <td>${tx.reference}</td>
            </tr>
        `;

        tableBody.innerHTML += row;
    });

})
.catch(error => {
    console.log("Dashboard Error:", error);
});


// ===============================
// LOGOUT
// ===============================

document.getElementById("logoutBtn")
.addEventListener("click", function () {

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    window.location.href = "login.html";
});