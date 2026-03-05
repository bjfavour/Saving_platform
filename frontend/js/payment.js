const token = localStorage.getItem("access");

if (!token) {
    window.location.href = "login.html";
}



const form = document.getElementById("paymentForm");

form.addEventListener("submit", function(e){

    e.preventDefault();


    const month = document.getElementById("month").value;
    const amount = document.getElementById("amount").value;
    const slip = document.getElementById("slip").files[0];


    const formData = new FormData();

    formData.append("month", month);
    formData.append("amount", amount);
    formData.append("slip", slip);



    fetch("http://127.0.0.1:8000/api/savings/payments/", {

        method: "POST",

        headers: {
            "Authorization": "Bearer " + token
        },

        body: formData

    })
    .then(response => {

        if (response.status === 403) {

            return response.json().then(data => {

                if (data.detail === "Subscription expired.") {
                    window.location.href = "subscription.html";
                }

            });

        }

        return response.json();

    })
    .then(data => {

        alert("Payment submitted successfully! Awaiting admin approval.");

        form.reset();

    })
    .catch(error => {

        console.log(error);
        alert("Error submitting payment");

    });

});