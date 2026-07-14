fetch("/api/settings", {

    method:"POST",

    headers:{
        "Content-Type":"application/json"
    },

    body:JSON.stringify({

        tahun:2026,

        triwulan:3

    })

})

document.addEventListener("DOMContentLoaded", () => {

    if (document.querySelector(".progress-bar")) {
        animateProgressBars();
    }

    if (document.querySelector(".clickable-row")) {
        enableClickableRows();
    }

    if (document.querySelector("#searchInput")) {
        enableSearch();
    }

});

function animateProgressBars() {

    document
        .querySelectorAll(".progress-bar")
        .forEach(bar => {

            const progress = bar.dataset.progress;

            bar.style.width = "0%";

            requestAnimationFrame(() => {

                bar.style.width = progress + "%";

            });

        });

}

function enableClickableRows() {

    // TODO
}

function enableSearch() {

    const input = document.getElementById("searchInput");

    const rows = document.querySelectorAll(".clickable-row");

    const tableBody = document.getElementById("tableBody");

    const emptyState = document.getElementById("emptyState");

    input.addEventListener("keyup", () => {

        const keyword = input.value
            .toLowerCase()
            .trim();

        let visibleRows = 0;

        rows.forEach(row => {

            const text = row.textContent.toLowerCase();

            const show = text.includes(keyword);

            row.style.display = show ? "" : "none";

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
