const map = initMap()
const routeData = getRouteData()

const routeCoords = extractCoordinatesFromRouteData(routeData)
const startCoord = routeCoords[0]
const endCoord = routeCoords.slice(-1)[0]

addMarker(startCoord, "start", map)
addMarker(endCoord, "end", map)

const totalDistance = getTotalDistance(map, routeCoords)

displayMap(routeData, totalDistance, map)

function initMap() {
    const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    const map = L.map('map')
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: attribution}).addTo(map);
    return map

}

function getRouteData() {
    return JSON.parse(document.getElementById('route-data').textContent);
}

function extractCoordinatesFromRouteData(routeData) {
    return routeData.features[0].geometry.coordinates
}

function displayMap(routeData, totalDistance, map) {
    const feature = L.geoJSON(routeData).bindPopup(function (layer) {
        return String(`${totalDistance.toFixed(2)} meters`);
    }).addTo(map);

    map.fitBounds(feature.getBounds(), {padding: [100, 100]});
}

function addMarker(coord, text, map) {
    L.marker([coord[1], coord[0]]).addTo(map).bindTooltip(text, {
        permanent: true,
    })
}

function getTotalDistance(map, routeCoords) {
    let totalDistance = 0
    for (let i = 1; i < routeCoords.length; i++) {
        totalDistance += map.distance(routeCoords[i], routeCoords[i - 1])
    }
    return totalDistance
}
