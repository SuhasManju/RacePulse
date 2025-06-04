import * as dateFns from 'date-fns';
import Chart from 'chart.js/auto';
import axios from 'axios';
import moment from 'moment-timezone';
import L from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet's default icon path issue with Webpack
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
});

// Make available globally
window.dateFns = dateFns;
window.Chart = Chart;
window.axios = axios;
window.Leaflet1 = L;
window.markerIcon = markerIcon;
window.markerShadow = markerShadow;


function formatUtcToLocal(utcString) {
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    // Format the UTC string to local time in the given time zone
    const formatted = moment(utcString).tz(timeZone).format("MMMM D, YYYY hh:mm A z");

    return formatted.replace("AM", "A.M.").replace("PM", "P.M.");
}
window.formatUtcToLocal = formatUtcToLocal;