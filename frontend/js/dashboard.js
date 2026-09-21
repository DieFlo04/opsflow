const API_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "../index.html";
}


let priorityChart = null;
let statusChart = null;
let systemChart = null;


/* =========================
   Usuario
   ========================= */

async function loadUser() {
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

        if (!response.ok) {
            throw new Error("Sesión inválida");
        }

        const user = await response.json();

        document.getElementById("user-info").textContent =
            `Bienvenido, ${user.name}. Rol: ${user.role}`;

    } catch (error) {
        console.error(
            "Error al cargar usuario:",
            error
        );

        localStorage.removeItem("access_token");

        window.location.href = "../index.html";
    }
}


/* =========================
   Métricas generales
   ========================= */

async function loadMetrics() {
    try {
        const response = await fetch(
            `${API_URL}/api/metrics/incidents`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                "No se pudieron obtener las métricas"
            );
        }

        const data = await response.json();

        document.getElementById(
            "total-incidents"
        ).textContent = data.total;

        document.getElementById(
            "open-incidents"
        ).textContent = data.open;

        document.getElementById(
            "in-progress-incidents"
        ).textContent = data.in_progress;

        document.getElementById(
            "resolved-incidents"
        ).textContent = data.resolved;

    } catch (error) {
        console.error(
            "Error al cargar métricas:",
            error
        );
    }
}


/* =========================
   Métricas por prioridad
   ========================= */

async function loadPriorityMetrics() {
    try {
        const response = await fetch(
            `${API_URL}/api/metrics/incidents/by-priority`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                "No se pudieron obtener las prioridades"
            );
        }

        const data = await response.json();

        renderPriorityMetrics(data);

        renderPriorityChart(data);

    } catch (error) {
        console.error(
            "Error al cargar métricas por prioridad:",
            error
        );

        document.getElementById(
            "priority-metrics"
        ).innerHTML =
            "<p>Error al cargar los datos.</p>";
    }
}


function renderPriorityMetrics(data) {
    const container =
        document.getElementById("priority-metrics");

    container.innerHTML = "";

    const priorities = [
        {
            key: "CRITICAL",
            label: "Crítica",
            className: "priority-critical"
        },
        {
            key: "HIGH",
            label: "Alta",
            className: "priority-high"
        },
        {
            key: "MEDIUM",
            label: "Media",
            className: "priority-medium"
        },
        {
            key: "LOW",
            label: "Baja",
            className: "priority-low"
        }
    ];

    priorities.forEach((priority) => {

        const count =
            data[priority.key] || 0;

        const item =
            document.createElement("div");

        item.className =
            "analytics-item";

        item.innerHTML = `
            <span class="${priority.className}">
                ${priority.label}
            </span>

            <strong>
                ${count}
            </strong>
        `;

        container.appendChild(item);
    });
}


function renderPriorityChart(data) {
    const context =
        document.getElementById("priority-chart");

    if (priorityChart) {
        priorityChart.destroy();
    }

    priorityChart = new Chart(
        context,
        {
            type: "doughnut",

            data: {
                labels: [
                    "Crítica",
                    "Alta",
                    "Media",
                    "Baja"
                ],

                datasets: [
                    {
                        data: [
                            data.CRITICAL || 0,
                            data.HIGH || 0,
                            data.MEDIUM || 0,
                            data.LOW || 0
                        ]
                    }
                ]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        }
    );
}


/* =========================
   Métricas por estado
   ========================= */

async function loadStatusMetrics() {
    try {
        const response = await fetch(
            `${API_URL}/api/metrics/incidents/by-status`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                "No se pudieron obtener los estados"
            );
        }

        const data = await response.json();

        renderStatusMetrics(data);

        renderStatusChart(data);

    } catch (error) {
        console.error(
            "Error al cargar métricas por estado:",
            error
        );

        document.getElementById(
            "status-metrics"
        ).innerHTML =
            "<p>Error al cargar los datos.</p>";
    }
}


function renderStatusMetrics(data) {
    const container =
        document.getElementById("status-metrics");

    container.innerHTML = "";

    const statuses = [
        {
            key: "OPEN",
            label: "Abierto",
            className: "status-open"
        },
        {
            key: "IN_PROGRESS",
            label: "En progreso",
            className: "status-in_progress"
        },
        {
            key: "RESOLVED",
            label: "Resuelto",
            className: "status-resolved"
        },
        {
            key: "CLOSED",
            label: "Cerrado",
            className: "status-closed"
        }
    ];

    statuses.forEach((status) => {

        const count =
            data[status.key] || 0;

        const item =
            document.createElement("div");

        item.className =
            "analytics-item";

        item.innerHTML = `
            <span class="${status.className}">
                ${status.label}
            </span>

            <strong>
                ${count}
            </strong>
        `;

        container.appendChild(item);
    });
}


function renderStatusChart(data) {
    const context =
        document.getElementById("status-chart");

    if (statusChart) {
        statusChart.destroy();
    }

    statusChart = new Chart(
        context,
        {
            type: "bar",

            data: {
                labels: [
                    "Abierto",
                    "En progreso",
                    "Resuelto",
                    "Cerrado"
                ],

                datasets: [
                    {
                        label: "Incidentes",

                        data: [
                            data.OPEN || 0,
                            data.IN_PROGRESS || 0,
                            data.RESOLVED || 0,
                            data.CLOSED || 0
                        ]
                    }
                ]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,

                        ticks: {
                            precision: 0
                        }
                    }
                },

                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        }
    );
}


/* =========================
   Análisis operativo
   ========================= */

async function loadIncidentAnalysis() {
    try {
        const response = await fetch(
            `${API_URL}/api/metrics/analysis`,
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
                "No se pudo obtener el análisis de incidentes"
            );
        }

        const data = await response.json();

        document.getElementById(
            "analysis-open"
        ).textContent =
            data.total_open_incidents;

        document.getElementById(
            "analysis-critical"
        ).textContent =
            data.critical_incidents;

        document.getElementById(
            "analysis-old"
        ).textContent =
            data.old_incidents;

        renderAlerts(data.alerts);

    } catch (error) {
        console.error(
            "Error al cargar análisis:",
            error
        );

        document.getElementById(
            "alerts-container"
        ).innerHTML =
            "<p>Error al cargar el análisis.</p>";
    }
}


function renderAlerts(alerts) {
    const container =
        document.getElementById("alerts-container");

    container.innerHTML = "";

    if (!alerts || alerts.length === 0) {

        container.innerHTML = `
            <div class="no-alerts">
                No hay alertas que requieran atención.
            </div>
        `;

        return;
    }

    alerts.forEach((alert) => {

        const alertElement =
            document.createElement("div");

        alertElement.className =
            `alert-item alert-${String(
                alert.severity
            ).toLowerCase()}`;

        alertElement.innerHTML = `
            <div class="alert-content">

                <strong>
                    ${escapeHtml(alert.type)}
                </strong>

                <p>
                    ${escapeHtml(alert.message)}
                </p>

            </div>

            <span class="alert-severity">
                ${escapeHtml(alert.severity)}
            </span>
        `;

        container.appendChild(alertElement);
    });
}


/* =========================
   Análisis de resolución
   ========================= */

async function loadResolutionMetrics() {

    try {

        const response = await fetch(
            `${API_URL}/api/metrics/incidents/average-resolution-time`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {

            localStorage.removeItem(
                "access_token"
            );

            window.location.href =
                "../index.html";

            return;
        }

        if (!response.ok) {
            throw new Error(
                "No se pudo obtener el tiempo promedio de resolución"
            );
        }

        const data =
            await response.json();

        const averageElement =
            document.getElementById(
                "average-resolution-time"
            );

        const average =
            data.average_resolution_hours;

        if (
            average !== null &&
            average !== undefined
        ) {

            averageElement.textContent =
                `${Number(average).toFixed(2)} h`;

        } else {

            averageElement.textContent =
                "Sin datos";
        }

    } catch (error) {

        console.error(
            "Error al cargar tiempo promedio de resolución:",
            error
        );

        document.getElementById(
            "average-resolution-time"
        ).textContent =
            "Error";
    }
}


async function loadResolutionTimes() {

    try {

        const response = await fetch(
            `${API_URL}/api/metrics/incidents/resolution-times`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {

            localStorage.removeItem(
                "access_token"
            );

            window.location.href =
                "../index.html";

            return;
        }

        if (!response.ok) {
            throw new Error(
                "No se pudieron obtener los tiempos de resolución"
            );
        }

        const data =
            await response.json();

        const tableBody =
            document.getElementById(
                "resolution-table-body"
            );

        tableBody.innerHTML = "";

        const incidents =
            Array.isArray(data)
                ? data
                : (
                    data.items ||
                    data.results ||
                    data.incidents ||
                    []
                );

        document.getElementById(
            "resolved-incidents-count"
        ).textContent =
            incidents.length;

        if (incidents.length === 0) {

            tableBody.innerHTML = `
                <tr>
                    <td colspan="3">
                        No hay incidentes resueltos.
                    </td>
                </tr>
            `;

            return;
        }

        incidents.forEach((incident) => {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td>
                    ${escapeHtml(
                        incident.title ||
                        `Incidente #${incident.id}`
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        incident.priority || "-"
                    )}
                </td>

                <td>
                    ${formatHours(
                        incident.resolution_hours
                    )}
                </td>
            `;

            tableBody.appendChild(row);
        });

    } catch (error) {

        console.error(
            "Error al cargar tiempos de resolución:",
            error
        );

        document.getElementById(
            "resolved-incidents-count"
        ).textContent =
            "Error";

        document.getElementById(
            "resolution-table-body"
        ).innerHTML = `
            <tr>
                <td colspan="3">
                    Error al cargar los datos.
                </td>
            </tr>
        `;
    }
}


/* =========================
   Análisis por sistema
   ========================= */

async function loadSystemMetrics() {

    try {

        const response = await fetch(
            `${API_URL}/api/metrics/incidents/by-system`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {

            localStorage.removeItem(
                "access_token"
            );

            window.location.href =
                "../index.html";

            return;
        }

        if (!response.ok) {
            throw new Error(
                "No se pudieron obtener los incidentes por sistema"
            );
        }

        const data =
            await response.json();

        renderSystemMetrics(data);

        renderSystemChart(data);

    } catch (error) {

        console.error(
            "Error al cargar métricas por sistema:",
            error
        );

        document.getElementById(
            "system-metrics-list"
        ).innerHTML =
            "<p>Error al cargar los datos.</p>";
    }
}


function normalizeSystemData(data) {

    if (Array.isArray(data)) {
        return data.map((item) => ({
            name:
                item.system_name ||
                item.name ||
                item.system ||
                "Sin sistema",

            count:
                item.count ??
                item.total ??
                item.incidents ??
                0
        }));
    }

    return Object.entries(data).map(
        ([name, count]) => ({
            name,
            count:
                typeof count === "number"
                    ? count
                    : Number(count) || 0
        })
    );
}


function renderSystemMetrics(data) {

    const container =
        document.getElementById(
            "system-metrics-list"
        );

    container.innerHTML = "";

    const systems =
        normalizeSystemData(data);

    if (systems.length === 0) {

        container.innerHTML = `
            <p>
                No hay datos de sistemas disponibles.
            </p>
        `;

        return;
    }

    systems.forEach((system) => {

        const item =
            document.createElement("div");

        item.className =
            "system-metric-item";

        item.innerHTML = `
            <span class="system-metric-name">
                ${escapeHtml(system.name)}
            </span>

            <span class="system-metric-count">
                ${system.count}
            </span>
        `;

        container.appendChild(item);
    });
}


function renderSystemChart(data) {

    const context =
        document.getElementById(
            "system-chart"
        );

    const systems =
        normalizeSystemData(data);

    if (systemChart) {
        systemChart.destroy();
    }

    if (systems.length === 0) {
        return;
    }

    systemChart = new Chart(
        context,
        {
            type: "bar",

            data: {
                labels: systems.map(
                    (system) => system.name
                ),

                datasets: [
                    {
                        label: "Incidentes",

                        data: systems.map(
                            (system) => system.count
                        )
                    }
                ]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,

                        ticks: {
                            precision: 0
                        }
                    }
                },

                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        }
    );
}


/* =========================
   Utilidades
   ========================= */

function formatHours(value) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(Number(value))
    ) {
        return "-";
    }

    return `${Number(value).toFixed(2)} h`;
}


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value === null ||
        value === undefined
            ? ""
            : String(value);

    return div.innerHTML;
}


/* =========================
   Eventos
   ========================= */

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


document.getElementById(
    "incidents-button"
).addEventListener(
    "click",
    () => {

        window.location.href =
            "incidents.html";
    }
);


/* =========================
   Carga inicial
   ========================= */

loadUser();

loadMetrics();

loadPriorityMetrics();

loadStatusMetrics();

loadIncidentAnalysis();

loadResolutionMetrics();

loadResolutionTimes();

loadSystemMetrics();