const API_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "../index.html";
}


let currentPage = 1;

const pageSize = 10;


async function loadIncidents() {

    const search = document.getElementById("search").value.trim();
    const status = document.getElementById("status").value;
    const priority = document.getElementById("priority").value;

    const params = new URLSearchParams();

    params.append("page", currentPage);
    params.append("page_size", pageSize);

    if (search) {
        params.append("search", search);
    }

    if (status) {
        params.append("status", status);
    }

    if (priority) {
        params.append("priority", priority);
    }

    try {

        const response = await fetch(
            `${API_URL}/api/incidents/?${params.toString()}`,
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
                "No se pudieron obtener los incidentes"
            );
        }

        const data = await response.json();

        renderIncidents(data);

    } catch (error) {

        console.error(
            "Error al cargar incidentes:",
            error
        );

        document.getElementById(
            "incident-count"
        ).textContent = "Error al cargar incidentes.";
    }
}


function renderIncidents(data) {

    const tableBody = document.getElementById(
        "incidents-table-body"
    );

    const emptyMessage = document.getElementById(
        "empty-message"
    );

    tableBody.innerHTML = "";

    document.getElementById(
        "incident-count"
    ).textContent =
        `${data.total} incidente(s) encontrado(s)`;


    if (data.items.length === 0) {

        emptyMessage.style.display = "block";

    } else {

        emptyMessage.style.display = "none";

        data.items.forEach((incident) => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${incident.id}</td>

                <td>${escapeHtml(incident.title)}</td>

                <td>
                    <span class="priority-${incident.priority.toLowerCase()}">
                        ${incident.priority}
                    </span>
                </td>

                <td>
                    <span class="status-${incident.status.toLowerCase()}">
                        ${incident.status}
                    </span>
                </td>

                <td>${incident.system_id}</td>

                <td>${incident.created_by}</td>
            `;

            row.style.cursor = "pointer";

            row.addEventListener(
                "click",
                () => {
                    window.location.href =
                        `incident-detail.html?id=${incident.id}`;
                }
            );

            tableBody.appendChild(row);

        });
    }


    document.getElementById(
        "page-info"
    ).textContent =
        `Página ${data.page} de ${data.total_pages}`;


    document.getElementById(
        "previous-button"
    ).disabled = data.page <= 1;


    document.getElementById(
        "next-button"
    ).disabled = data.page >= data.total_pages;
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


document.getElementById(
    "filter-button"
).addEventListener(
    "click",
    () => {

        currentPage = 1;

        loadIncidents();
    }
);


document.getElementById(
    "previous-button"
).addEventListener(
    "click",
    () => {

        if (currentPage > 1) {

            currentPage--;

            loadIncidents();
        }
    }
);


document.getElementById(
    "next-button"
).addEventListener(
    "click",
    () => {

        currentPage++;

        loadIncidents();
    }
);


document.getElementById(
    "back-button"
).addEventListener(
    "click",
    () => {

        window.location.href = "dashboard.html";
    }
);


document.getElementById(
    "logout-button"
).addEventListener(
    "click",
    () => {

        localStorage.removeItem("access_token");

        window.location.href = "../index.html";
    }
);


loadIncidents();

document.getElementById(
    "new-incident-button"
).addEventListener(
    "click",
    () => {

        window.location.href =
            "create-incident.html";
    }
);