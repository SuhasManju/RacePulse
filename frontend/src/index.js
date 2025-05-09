import * as dateFns from 'date-fns';
import Chart from 'chart.js/auto';
import axios from 'axios';
import moment from 'moment-timezone';

window.dateFns = dateFns;
window.Chart = Chart;
window.axios = axios;


function formatUtcToLocal(utcString) {
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    // Format the UTC string to local time in the given time zone
    const formatted = moment(utcString).tz(timeZone).format("MMMM D, YYYY hh:mm A z");

    return formatted.replace("AM", "A.M.").replace("PM", "P.M.");
}
window.formatUtcToLocal = formatUtcToLocal;