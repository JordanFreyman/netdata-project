const chartConfigs = [
    { key: 'cpu', label: 'CPU Usage' },
    { key: 'memory', label: 'Memory Usage' },
    { key: 'disk', label: 'Disk Usage' },
    { key: 'network', label: 'Network Usage' }
];

const charts = {};

function createOrUpdateMachineCharts(machine, metrics, range) {
    // Check if the machine has at least one non-null metric data point
    const hasValidData = Object.values(metrics).some(metricData =>
        Array.isArray(metricData) && metricData.some(p => p.value !== null)
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
        const data = metrics[key] || [];
        const canvas = document.getElementById(`${key}Chart-${machine}`);
        const ctx = canvas.getContext('2d');

        const validPoints = data.filter(p => p.value !== null);
        const labels = validPoints.map(p => {
            const date = new Date(p.timestamp);
            return range === '7d' ? date.toLocaleString() : date.toLocaleTimeString();
        });
        const values = validPoints.map(p => p.value);

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
    const container = document.getElementById('chartsContainer');
    if (!container) return;

    container.innerHTML = '';
    Object.keys(charts).forEach(k => delete charts[k]);

    const allData = {}; // ← group by machine and metric

    let completed = 0;

    chartConfigs.forEach(({ key }) => {
        fetch(`/api/metrics/${key}?range=${selectedRange}`)
            .then(response => response.json())
            .then(data => {
                for (const machine in data) {
                    if (!allData[machine]) allData[machine] = {};
                    allData[machine][key] = data[machine]; // ✅ assign correct metric
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

fetchAndUpdateCharts();
setInterval(fetchAndUpdateCharts, 60 * 1000);
document.getElementById('rangeSelect')?.addEventListener('change', () => {
    document.querySelector('.charts-container').innerHTML = '';
    Object.keys(charts).forEach(k => delete charts[k]);
    fetchAndUpdateCharts();
});
