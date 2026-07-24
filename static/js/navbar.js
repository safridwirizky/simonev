document.addEventListener("DOMContentLoaded", function () {

    const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
    };

    document.getElementById("current-date").textContent =
        new Date().toLocaleDateString("id-ID", options);

});
