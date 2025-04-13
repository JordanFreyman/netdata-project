const chartConfigs = [
    { id: 'cpuChart', endpoint: '/api/metrics/cpu', label: 'CPU Usage' },
    { id: 'memoryChart', endpoint: '/api/metrics/memory', label: 'Memory Usage' },
    { id: 'diskChart', endpoint: '/api/metrics/disk', label: 'Disk Usage' },
    { id: 'networkChart', endpoint: '/api/metrics/network', label: 'Network Usage' }
];

const charts = {};

function createOrUpdateChart(id, data, label) {
    const labels = data.map(point => new Date(point.timestamp).toLocaleTimeString());
    const values = data.map(point => point.value);
    const ctx = document.getElementById(id).getContext('2d');

    if (charts[id]) {
        charts[id].data.labels = labels;
        charts[id].data.datasets[0].data = values;
        charts[id].update();
    } else {
        charts[id] = new Chart(ctx, {
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
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

function fetchAndUpdateCharts() {
    chartConfigs.forEach(({ id, endpoint, label }) => {
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                createOrUpdateChart(id, data, label);
            })
            .catch(error => {
                console.error(`Error loading ${label}:`, error);
            });
    });
}

fetchAndUpdateCharts();

setInterval(fetchAndUpdateCharts, 60 * 1000);
