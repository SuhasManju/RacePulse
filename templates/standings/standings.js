function makeChart(ctxId, labels, data) {
    const ctx = document.getElementById(ctxId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,   // ✅ Required for x-axis labels
            datasets: data
        },
        options: {
            responsive: true,
            parsing: false, // Required if you're using custom x/y data format
            scales: {
                x: {
                    type: 'category',
                    title: { display: true, text: 'Race' }
                },
                y: {
                    title: { display: true, text: 'Points' }
                }
            }
        }
    });
}


const driverData = JSON.parse(document.getElementById("driver-data").textContent);
const lables = JSON.parse(document.getElementById("labels").textContent);
const driverDatasets = driverData.map(driver => ({
    label: driver.driverName,
    data: driver.pointsCumSum.map(([race, points]) => ({ x: race, y: points })),
    borderColor: driver.color,
    tension: 0.3,
    fill: false
}));

const teamData = JSON.parse(document.getElementById("team-data").textContent);
const teamDatasets = teamData.map(team => ({
    label: team.teamName,
    data: team.pointsCumSum.map(([race, points]) => ({ x: race, y: points })),
    borderColor: team.color,
    tension: 0.3,
    fill: false
}));


makeChart("myChart", lables, driverDatasets)
makeChart("myChartTeam", lables, teamDatasets)