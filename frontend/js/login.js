document.getElementById("loginForm")
.addEventListener("submit", function (e) {

    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const messageBox = document.getElementById("loginMessage");

    fetch("http://127.0.0.1:8000/api/auth/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.access) {

            // Save tokens
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            messageBox.innerHTML =
                "<span style='color:green;'>Login successful! Redirecting...</span>";

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1000);

        } else {

            messageBox.innerHTML =
                "<span style='color:red;'>Invalid credentials or not approved.</span>";
        }

    })
    .catch(error => {
        console.log(error);
    });

});