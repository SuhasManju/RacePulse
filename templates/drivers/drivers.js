function makeChart(ctxId, rawData) {
    const ctx = document.getElementById(ctxId).getContext('2d');

    const formattedData = rawData.map(entry => ({
        x: entry.year,
        y: entry.position,
        points: parseFloat(entry.points)
    }));

    return new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Driver Position Over Years',
                data: formattedData,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            parsing: false,
            indexAxis: 'x',
            scales: {
                x: {
                    type: 'linear', // allows duplicate years
                    title: {
                        display: true,
                        text: 'Year'
                    },
                    ticks: {
                        stepSize: 1,
                        callback: function (value) {
                            return value.toString(); // convert number to year-like string
                        }
                    }
                },
                y: {
                    reverse: true,
                    title: {
                        display: true,
                        text: 'Position'
                    },
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const d = context.raw;
                            return `Year: ${d.x}, Position: ${d.y}, Points: ${d.points}`;
                        }
                    }
                }
            }
        }
    });
}


const driverData = JSON.parse(document.getElementById("driver-data").textContent);

makeChart("myChartDriver", driverData);