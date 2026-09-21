const API_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "../index.html";
}


const params = new URLSearchParams(
    window.location.search
);

const incidentId = params.get("id");

let currentIncident = null;


async function loadIncident() {

    if (!incidentId) {

        showError(
            "No se especificó un incidente."
        );

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/api/incidents/${incidentId}`,
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


        if (response.status === 404) {

            showError(
                "El incidente no existe."
            );

            return;
        }


        if (!response.ok) {

            throw new Error(
                "No se pudo obtener el incidente."
            );
        }


        const incident = await response.json();

        renderIncident(incident);

    } catch (error) {

        console.error(
            "Error al cargar incidente:",
            error
        );

        showError(
            "Ocurrió un error al cargar el incidente."
        );
    }
}


function renderIncident(incident) {
    currentIncident = incident; 

    document.getElementById(
        "loading-message"
    ).style.display = "none";


    document.getElementById(
        "incident-detail"
    ).style.display = "block";


    document.getElementById(
        "incident-id"
    ).textContent =
        `INCIDENTE #${incident.id}`;


    document.getElementById(
        "incident-title"
    ).textContent =
        incident.title;


    document.getElementById(
        "incident-description"
    ).textContent =
        incident.description;


    document.getElementById(
        "incident-priority"
    ).textContent =
        incident.priority;


    document.getElementById(
        "incident-status"
    ).textContent =
        incident.status;


    document.getElementById(
        "incident-system"
    ).textContent =
        incident.system_id;


    document.getElementById(
        "incident-category"
    ).textContent =
        incident.category_id;


    document.getElementById(
        "incident-created-by"
    ).textContent =
        incident.created_by;


    document.getElementById(
        "incident-assigned-to"
    ).textContent =
        incident.assigned_to ?? "Sin asignar";


    document.getElementById(
        "incident-created-at"
    ).textContent =
        formatDate(incident.created_at);


    document.getElementById(
        "incident-updated-at"
    ).textContent =
        formatDate(incident.updated_at);


    if (incident.resolved_at) {

        document.getElementById(
            "resolved-section"
        ).style.display = "block";


        document.getElementById(
            "incident-resolved-at"
        ).textContent =
            formatDate(incident.resolved_at);
    }
}


function formatDate(dateString) {

    if (!dateString) {
        return "N/A";
    }

    return new Date(dateString).toLocaleString(
        "es-MX"
    );
}


function showError(message) {

    document.getElementById(
        "loading-message"
    ).style.display = "none";


    const errorMessage =
        document.getElementById("error-message");

    errorMessage.textContent = message;

    errorMessage.style.display = "block";
}


document.getElementById(
    "back-button"
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


loadIncident();

document.getElementById(
    "edit-button"
).addEventListener(
    "click",
    () => {

        if (!currentIncident) {
            return;
        }

        document.getElementById(
            "edit-section"
        ).style.display = "block";

        document.getElementById(
            "edit-title"
        ).value = currentIncident.title;

        document.getElementById(
            "edit-description"
        ).value = currentIncident.description;

        document.getElementById(
            "edit-priority"
        ).value = currentIncident.priority;

        document.getElementById(
            "edit-status"
        ).value = currentIncident.status;

        document.getElementById(
            "edit-assigned-to"
        ).value =
            currentIncident.assigned_to ?? "";
    }
);


document.getElementById(
    "cancel-edit"
).addEventListener(
    "click",
    () => {

        document.getElementById(
            "edit-section"
        ).style.display = "none";

        document.getElementById(
            "edit-message"
        ).textContent = "";
    }
);


document.getElementById(
    "edit-form"
).addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const message =
            document.getElementById(
                "edit-message"
            );

        message.textContent =
            "Guardando cambios...";


        const updateData = {
            title: document.getElementById(
                "edit-title"
            ).value,

            description: document.getElementById(
                "edit-description"
            ).value,

            priority: document.getElementById(
                "edit-priority"
            ).value,

            status: document.getElementById(
                "edit-status"
            ).value
        };


        const assignedTo =
            document.getElementById(
                "edit-assigned-to"
            ).value;


        if (assignedTo) {

            updateData.assigned_to =
                Number(assignedTo);
        }


        try {

            const response = await fetch(
                `${API_URL}/api/incidents/${incidentId}`,
                {
                    method: "PUT",

                    headers: {
                        "Authorization":
                            `Bearer ${token}`,

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(updateData)
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
                    "No tienes permisos para actualizar este incidente.";

                return;
            }


            if (!response.ok) {

                message.textContent =
                    data.detail ||
                    "No se pudieron guardar los cambios.";

                return;
            }


            message.textContent =
                "Cambios guardados correctamente.";


            setTimeout(
                () => {
                    window.location.reload();
                },
                800
            );

        } catch (error) {

            console.error(
                "Error al actualizar incidente:",
                error
            );

            message.textContent =
                "Error de conexión con el servidor.";
        }
    }
);