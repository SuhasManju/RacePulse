const searchElement = document.getElementById("searchItem");
const dropdown = document.getElementById("dropdownResults");

searchElement.addEventListener("input", async function (event) {
    const searchItem = event.target.value.trim();

    if (!searchItem) {
        dropdown.classList.add("hidden");
        dropdown.innerHTML = "";
        return;
    }

    try {
        const res = await axios.get(`/search/?search=${searchItem}`);
        const data = res.data;
        const circuits = data.circuits || [];
        const drivers = data.drivers || [];
        const teams = data.teams || [];

        let html = "";

        if (drivers.length) {
            html += `<div class="px-3 py-1 text-xs font-bold text-gray-500 uppercase">Drivers</div>`;
            html += drivers.map(d =>
                `<div class="px-3 py-2 hover:bg-gray-100 cursor-pointer" onclick="window.location.href='${d.link}'">${d.name}</div>`
            ).join("");
        }

        if (teams.length) {
            html += `<div class="px-3 py-1 text-xs font-bold text-gray-500 uppercase mt-2">Teams</div>`;
            html += teams.map(t =>
                `<div class="px-3 py-2 hover:bg-gray-100 cursor-pointer" onclick="window.location.href='${t.link}'">${t.name}</div>`
            ).join("");
        }

        if (circuits.length) {
            html += `<div class="px-3 py-1 text-xs font-bold text-gray-500 uppercase mt-2">Circuits</div>`;
            html += circuits.map(c =>
                `<div class="px-3 py-2 hover:bg-gray-100 cursor-pointer" onclick="window.location.href='${c.link}'">${c.name}</div>`
            ).join("");
        }

        dropdown.innerHTML = html || `<div class="p-2 text-gray-500">No results found</div>`;
        dropdown.classList.remove("hidden");

    } catch (err) {
        console.error("Search failed:", err);
        dropdown.innerHTML = `<div class="p-2 text-red-500">Error fetching results</div>`;
        dropdown.classList.remove("hidden");
    }
});

document.addEventListener("keydown", function (e) {
    // Check if Ctrl + K is pressed
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();

        const searchInput = document.getElementById("searchItem");

        // Show and focus the input
        searchInput.style.display = "block";
        searchInput.focus();
    }
});

