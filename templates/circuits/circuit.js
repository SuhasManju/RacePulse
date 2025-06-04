function initMap() {
    const coOrdinates = JSON.parse("{{circuitData.coOrdinates|safe|escapejs}}")

    const map = Leaflet1.map('map').setView(coOrdinates, 13);

    Leaflet1.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    const marker = Leaflet1.marker(coOrdinates).addTo(map);

    setTimeout(() => {
        map.invalidateSize();
    }, 300);
}

document.addEventListener('DOMContentLoaded', initMap);

