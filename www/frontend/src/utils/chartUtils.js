import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    CategoryScale,
    Filler,
} from 'chart.js';

Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    CategoryScale,
    Filler
);

export function createChart(canvas, stock, isModal = false) {
    const ctx = canvas.getContext('2d');
    const data = stock.baseData || generateRandomData();
    const labels = data.map((_, index) => `Day ${index + 1}`);
    const datasets = [
        {
            label: `${stock.name} Price`,
            data: data,
            borderColor: stock.change >= 0 ? 'green' : 'red',
            backgroundColor:
                stock.change >= 0
                    ? 'rgba(0, 255, 0, 0.2)'
                    : 'rgba(255, 0, 0, 0.2)',
            fill: true,
            pointRadius: 0,
        },
    ];

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: isModal,
                },
                title: {
                    display: false,
                },
            },
            elements: {
                line: {
                    tension: 0.4,
                },
            },
            scales: {
                x: {
                    display: isModal,
                },
                y: {
                    display: isModal,
                },
            },
        },
    });
}

function generateRandomData() {
    const totalDays = 30;
    return Array.from({ length: totalDays }, () => Math.random() * 100 + 100);
}
