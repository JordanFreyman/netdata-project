const chartConfigs = [
    { key: 'cpu', label: 'CPU Usage' },
    { key: 'memory', label: 'Memory Usage' },
    { key: 'disk', label: 'Disk Usage' },
    { key: 'network', label: 'Network Usage' }
];

const charts = {};

function createOrUpdateMachineCharts(machine, metrics, range) {
    const hasValidData = Object.values(metrics).some(metricData =>
        Array.isArray(metricData) && metricData.length > 0 && metricData.some(p => p.value !== null)
    );

    if (!hasValidData) {
        console.log(`Skipping ${machine} — no valid data`);
        return;
    }

    const containerId = `charts-${machine}`;
    let container = document.getElementById(containerId);

    if (!container) {
        const dashboard = document.querySelector('.charts-container');
        container = document.createElement('div');
        container.id = containerId;
        container.className = 'machine-section';
        container.innerHTML = `<h2>Machine: ${machine}</h2>`;
        dashboard.appendChild(container);

        chartConfigs.forEach(({ key, label }) => {
            const card = document.createElement('div');
            card.className = 'chart-card';
            card.innerHTML = `
                <h3>${label}</h3>
                <div class="chart-wrapper">
                    <canvas id="${key}Chart-${machine}"></canvas>
                </div>
            `;
            container.appendChild(card);
        });
    }

    chartConfigs.forEach(({ key, label }) => {
        const data = Array.isArray(metrics[key]) ? metrics[key].filter(p => p.value !== null) : [];
        const canvas = document.getElementById(`${key}Chart-${machine}`);
        const ctx = canvas.getContext('2d');

        const labels = data.map(p => {
            const date = new Date(p.timestamp);
            return range === '7d' ? date.toLocaleString() : date.toLocaleTimeString();
        });

        const values = data.map(p => p.value);

        if (charts[`${key}-${machine}`]) {
            charts[`${key}-${machine}`].data.labels = labels;
            charts[`${key}-${machine}`].data.datasets[0].data = values;
            charts[`${key}-${machine}`].update();
        } else {
            charts[`${key}-${machine}`] = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        data: values,
                        borderWidth: 2,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.3,
                        fill: true,
                        spanGaps: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,
                    scales: { y: { beginAtZero: true } }
                }
            });
        }
    });
}

function fetchAndUpdateCharts() {
    const selectedRange = document.getElementById('rangeSelect')?.value || '1h';
    const container = document.querySelector('.charts-container');
    if (!container) return;

    container.innerHTML = '';
    Object.keys(charts).forEach(k => delete charts[k]);

    const allData = {};
    let completed = 0;

    chartConfigs.forEach(({ key }) => {
        fetch(`/api/metrics/${key}?range=${selectedRange}`)
            .then(response => response.json())
            .then(data => {
                // ✅ Skip if the response is not an object (e.g., if it's an array or invalid)
                if (typeof data !== 'object' || Array.isArray(data)) {
                    console.error(`Invalid data structure for ${key}:`, data);
                    return;
                }

                // Merge the data into allData
                for (const machine of Object.keys(data)) {
                    if (!allData[machine]) allData[machine] = {};
                    allData[machine][key] = data[machine];
                }

                completed++;
                if (completed === chartConfigs.length) {
                    for (const machine in allData) {
                        createOrUpdateMachineCharts(machine, allData[machine], selectedRange);
                    }
                }
            })
            .catch(error => {
                console.error(`Error loading ${key}:`, error);
            });
    });
}

window.addEventListener('error', function(e) {
    console.error("JS error detected:", e.message, "at", e.filename, ":", e.lineno);
});

fetchAndUpdateCharts();
setInterval(fetchAndUpdateCharts, 60 * 1000);
document.getElementById('rangeSelect')?.addEventListener('change', () => {
    document.querySelector('.charts-container').innerHTML = '';
    Object.keys(charts).forEach(k => delete charts[k]);
    fetchAndUpdateCharts();
});
