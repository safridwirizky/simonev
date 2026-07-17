function renderChart(
    container,
    options
) {

    if (!container) {
        return;
    }

    new ApexCharts(
        container,
        options
    ).render();

}
