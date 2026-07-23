document.addEventListener("DOMContentLoaded", () => {

    enableClickableRows();

    enableSearch();

});

function enableClickableRows() {

    document
        .querySelectorAll(".clickable-row")
        .forEach(row => {

            row.addEventListener("click", () => {

                window.location = row.dataset.href;

            });

        });

}

function enableSearch() {

    const input = document.getElementById(
        "searchInput"
    );

    if (!input) {
        return;
    }

    const rows = document.querySelectorAll(
        ".clickable-row"
    );

    const emptyState = document.getElementById(
        "emptyState"
    );

    input.addEventListener("keyup", () => {

        const keyword = input.value
            .toLowerCase()
            .trim();

        let visibleRows = 0;

        rows.forEach(row => {

            const show = row.textContent
                .toLowerCase()
                .includes(keyword);

            row.style.display = show
                ? ""
                : "none";

            if (show) {
                visibleRows++;
            }

        });

        emptyState.classList.toggle(
            "d-none",
            visibleRows > 0
        );

    });

}

document
    .querySelectorAll("[data-triwulan]")
    .forEach(item => {

        item.addEventListener("click", async () => {

            const triwulan = item.dataset.triwulan;

            const response = await fetch(
                "/api/settings/triwulan",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        triwulan: triwulan
                    })
                }
            );

            if (!response.ok) {
                alert("Gagal mengubah triwulan.");
                return;
            }

            location.reload();

        });

    });
