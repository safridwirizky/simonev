document.addEventListener("DOMContentLoaded", () => {

    animateProgressBars();

});

function animateProgressBars() {

    document
        .querySelectorAll(".progress-bar")
        .forEach(bar => {

            const progress = Number(
                bar.dataset.progress || 0
            );

            bar.style.width = "0%";

            requestAnimationFrame(() => {

                bar.style.width = `${progress}%`;

            });

        });

}
