const API_URL = "http://127.0.0.1:8000";

const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");


loginForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    loginMessage.textContent = "Iniciando sesión...";

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    try {

        const response = await fetch(
            `${API_URL}/api/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },

                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Error al iniciar sesión"
            );
        }

        localStorage.setItem(
            "access_token",
            data.access_token
        );

        loginMessage.textContent = "Inicio de sesión exitoso.";

        console.log("Token recibido correctamente.");

        window.location.href = "pages/dashboard.html";

    } catch (error) {

        loginMessage.textContent = error.message;

    }

});