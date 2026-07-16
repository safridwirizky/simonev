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
