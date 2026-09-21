const API_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "../index.html";
}


let currentUser = null;


async function loadCurrentUser() {

    try {

        const response = await fetch(
            `${API_URL}/api/auth/me`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );


        if (response.status === 401) {

            localStorage.removeItem("access_token");

            window.location.href = "../index.html";

            return;
        }


        if (!response.ok) {
            throw new Error(
                "No se pudo obtener el usuario."
            );
        }


        currentUser = await response.json();

    } catch (error) {

        console.error(
            "Error al obtener usuario:",
            error
        );
    }
}


document.getElementById(
    "create-incident-form"
).addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        const message =
            document.getElementById(
                "create-message"
            );


        message.textContent =
            "Creando incidente...";


        if (!currentUser) {

            message.textContent =
                "No se pudo identificar al usuario.";

            return;
        }


        const incidentData = {

            title: document.getElementById(
                "title"
            ).value.trim(),

            description: document.getElementById(
                "description"
            ).value.trim(),

            priority: document.getElementById(
                "priority"
            ).value,

            system_id: Number(
                document.getElementById(
                    "system-id"
                ).value
            ),

            category_id: Number(
                document.getElementById(
                    "category-id"
                ).value
            ),

            created_by: currentUser.id
        };


        try {

            const response = await fetch(
                `${API_URL}/api/incidents/`,
                {
                    method: "POST",

                    headers: {
                        "Authorization":
                            `Bearer ${token}`,

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        incidentData
                    )
                }
            );


            const data = await response.json();


            if (response.status === 401) {

                localStorage.removeItem(
                    "access_token"
                );

                window.location.href =
                    "../index.html";

                return;
            }


            if (response.status === 403) {

                message.textContent =
                    "No tienes permisos para crear incidentes.";

                return;
            }


            if (!response.ok) {

                message.textContent =
                    data.detail ||
                    "No se pudo crear el incidente.";

                return;
            }


            message.textContent =
                "Incidente creado correctamente.";


            setTimeout(
                () => {

                    window.location.href =
                        `incident-detail.html?id=${data.id}`;

                },
                800
            );


        } catch (error) {

            console.error(
                "Error al crear incidente:",
                error
            );

            message.textContent =
                "Error de conexión con el servidor.";
        }
    }
);


document.getElementById(
    "cancel-button"
).addEventListener(
    "click",
    () => {

        window.location.href =
            "incidents.html";
    }
);


document.getElementById(
    "logout-button"
).addEventListener(
    "click",
    () => {

        localStorage.removeItem(
            "access_token"
        );

        window.location.href =
            "../index.html";
    }
);


loadCurrentUser();