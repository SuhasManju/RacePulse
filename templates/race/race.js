

document.addEventListener('htmx:beforeRequest', function (e) {
    if (!e.target.matches('.tab-button')) return;

    // Clear existing active state
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('text-blue-600', 'border-blue-500');
        btn.classList.add('text-gray-700', 'border-transparent');
    });

    // Set active state on clicked button
    e.target.classList.remove('text-gray-700', 'border-transparent');
    e.target.classList.add('text-blue-600', 'border-blue-500');
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".local-time").forEach(el => {
        const utc = el.dataset.utc;
        if (!utc) return;

        try {
            el.textContent = formatUtcToLocal(utc);
        } catch (e) {
            console.error("Failed to format UTC:", utc, e);
            el.textContent = utc; // fallback
        }
    });
});


function timeInterval() {
    const nextEventTime = new Date("{{ nextEvent|safe|escapejs }}");
    const now = new Date();
    const duration = dateFns.intervalToDuration({ 'start': now, 'end': nextEventTime });

    var days = duration.days | 0;
    var hours = duration.hours | 0;
    var minutes = duration.minutes | 0;
    var seconds = duration.seconds | 0;
    var months = duration.months | 0;

    if (days < 10) {
        days = `0${days}`;
    }
    if (hours < 10) {
        hours = `0${hours}`;
    }
    if (minutes < 10) {
        minutes = `0${minutes}`;
    }
    if (seconds < 10) {
        seconds = `0${seconds}`;
    }
    if (months < 10) {
        months = `0${months}`;
    }

    let countdownElements = document.getElementsByClassName("countdown-element");

    // Loop through the elements and update their content
    for (let i = 0; i < countdownElements.length; i++) {
        let className = countdownElements[i].classList[1]; // Get the second class name
        switch (className) {
            case "days":
                countdownElements[i].innerHTML = days;
                break;
            case "hours":
                countdownElements[i].innerHTML = hours;
                break;
            case "minutes":
                countdownElements[i].innerHTML = minutes;
                break;
            case "seconds":
                countdownElements[i].innerHTML = seconds;
                break;
            case "months":
                countdownElements[i].innerHTML = months;
                break;
            default:
                break;

        }
    }
}



timeInterval()

setInterval(timeInterval, 1000)