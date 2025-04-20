const chartConfigs = [
    { id: 'cpuChart', endpoint: '/api/metrics/cpu', label: 'CPU Usage' },
    { id: 'memoryChart', endpoint: '/api/metrics/memory', label: 'Memory Usage' },
    { id: 'diskChart', endpoint: '/api/metrics/disk', label: 'Disk Usage' },
    { id: 'networkChart', endpoint: '/api/metrics/network', label: 'Network Usage' }
];

const charts = {};

function createOrUpdateChart(id, groupedData, label) {
    const container = document.getElementById(id)?.parentElement;
    const canvas = document.getElementById(id);

    if (!canvas || !container) {
        console.error(`Canvas or container not found for chart ID: ${id}`);
        return;
    }

    const validPoints = [];
    for (const machine in groupedData) {
        if (machine === "127.0.0.1") { // Only use your local machine for now
            for (const point of groupedData[machine]) {
                if (point.value !== null) {
                    validPoints.push(point);
                }
            }
        }
    }

    if (validPoints.length === 0){
        canvas.style.display = 'none';
        if (!container.querySelector('.fallback-message')) {
            const fallback = document.createElement('p');
            fallback.textContent = `No data available for ${label}.`;
            fallback.style.color = 'red';
            fallback.classList.add('fallback-message');
            container.appendChild(fallback);
        }
        return;
}


    canvas.style.display = 'block';
    const oldFallback = container.querySelector('.fallback-message');
    if (oldFallback) oldFallback.remove();

    const values = validPoints.map(p => p.value);

    const range = document.getElementById('rangeSelect')?.value || '1h';
    const labels = validPoints.map(p => {
        const date = new Date(p.timestamp);
        return range === '7d'
            ? date.toLocaleString()
            : date.toLocaleTimeString();
    });

    const ctx = canvas.getContext('2d');

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
    const selectedRange = document.getElementById('rangeSelect')?.value || '1h';

    chartConfigs.forEach(({ id, endpoint, label }) => {
        fetch(`${endpoint}?range=${selectedRange}`)
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
document.getElementById('rangeSelect')?.addEventListener('change', fetchAndUpdateCharts);
