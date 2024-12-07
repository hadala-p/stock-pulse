import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    CategoryScale,
    Filler,
    Tooltip,
} from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    CategoryScale,
    Filler,
    Tooltip,
    zoomPlugin
);

export function createChart(canvas, stock, isModal = false, numOfPastDays = 30) {
    if (numOfPastDays < 0) 
    {
        numOfPastDays = Math.min(stock.baseData.length, 720)
    }
    const lerp = (a, b, t) => a + (b - a) * t;
    const ctx = canvas.getContext('2d');
    let baseData = stock.baseData;
    if (numOfPastDays > 0) 
    {
        baseData = baseData.slice(-numOfPastDays);
    }
    baseData = baseData.map((value) => Number(value));
    const data = baseData.concat(new Array(stock.predictedData.length).fill(null));
    const lastBaseDataValue = Number(stock.baseData[stock.baseData.length - 1]);
    const predictedDataRaw = stock.predictedData.map((value) => Number(value));
    let predictedDataBlended = []
    for (let i = 0; i < predictedDataRaw.length; i++) {
        let t = i < 10 ? i / 10.0 : 1; 
        const value = lerp(lastBaseDataValue, predictedDataRaw[i], t);
        predictedDataBlended.push(value);
    }

    const predictedData = new Array(baseData.length - 1).fill(null).concat(predictedDataBlended);
    const labels = baseData.map((_, index) => `Day ${index - baseData.length}`).concat(predictedDataRaw.map((_, index) => `Day ${index + 1}`));
    const stockChange = stock.predictedData[stock.predictedData.length - 1] - lastBaseDataValue > 0;
    const maxValue = Math.max(...baseData, ...predictedDataBlended);
    const datasets = [
        {
            label: `Price`,
            data: data,
            borderColor: 'rgba(0, 0, 0, 0.2)',
            backgroundColor: 'rgba(0, 0, 0, 0.2)',
            fill: true,
            pointRadius: 0,
        },
        {
            label: `Predicted price`,
            data: predictedData,
            borderColor: stockChange ? 'green' : 'red',
            backgroundColor: stockChange ? 'rgba(0, 255, 0, 0.2)' : 'rgba(255, 0, 0, 0.2)',
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
            animation: {
                duration: (isModal ? 0 : 1000),
            },
            plugins: {
                legend: {
                    display: isModal,
                },
                title: {
                    display: false,
                },
                zoom: {
                    pan: {
                        enabled: isModal,
                        mode: 'x',
                    },
                    zoom: {
                        wheel: {
                            enabled: isModal,
                        },
                        pinch: {
                            enabled: isModal,
                        },
                        mode: 'x',
                    },
                },
                tooltip: {
                    enabled: true,
                    mode: 'nearest',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += `$ ${context.parsed.y.toFixed(2)}`;
                            }
                            return label;
                        }
                    }
                }
            },
            elements: {
                line: {
                    tension: 0.4,
                },
            },
            scales: {
                x: {
                    display: isModal,
                    min: labels.length - (isModal ? 150 : 60),
                    max: labels.length,
                },
                y: {
                    display: isModal,
                    beginAtZero: isModal,
                    suggestedMax: maxValue,
                    ticks: {
                        callback: function(value) {
                            return `$ ${value}`;
                        }
                    }
                },
            },
        },
    });
}