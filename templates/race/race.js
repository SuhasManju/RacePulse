

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