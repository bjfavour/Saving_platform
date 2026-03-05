document.getElementById("registerForm")
.addEventListener("submit", function (e) {

    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const telephone = document.getElementById("telephone").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    const messageBox = document.getElementById("registerMessage");

    if (password !== confirmPassword) {
        messageBox.innerHTML =
            "<span style='color:red;'>Passwords do not match</span>";
        return;
    }

    fetch("http://127.0.0.1:8000/api/accounts/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            email: email,
            telephone: telephone,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.username || data.email || data.telephone) {
            messageBox.innerHTML =
                "<span style='color:red;'>" +
                JSON.stringify(data) +
                "</span>";
        } else {
            messageBox.innerHTML =
                "<span style='color:green;'>Registration successful! Wait for admin approval.</span>";

            document.getElementById("registerForm").reset();
        }

    })
    .catch(error => {
        console.log(error);
    });

});