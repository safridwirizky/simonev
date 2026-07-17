function initAnggaranChart() {

    const container = document.getElementById(
        "anggaranChart"
    );

    if (!container) {
        return;
    }

    const chart = JSON.parse(
        container.dataset.chart
    );

    const data = getAnggaranData(
        chart
    );

    const options = buildAnggaranChart(
        data
    );

    renderChart(
        container,
        options
    );

}

function getAnggaranData(chart) {

    return {

        categories: chart.triwulan.map(
            item => item.periode
        ),

        target: chart.triwulan.map(
            item => item.target.value
        ),

        realisasi: chart.triwulan.map(
            item => item.realisasi.value
        )

    };

}

function buildAnggaranChart(data) {

    return {

        chart: {

            type: "bar",

            height: 380,

            toolbar: {

                show: false

            }

        },

        series: [

            {

                name: "Target",

                data: data.target

            },

            {

                name: "Realisasi",

                data: data.realisasi

            }

        ],

        xaxis: {

            categories: data.categories

        },

        plotOptions: {

            bar: {

                horizontal: false,

                columnWidth: "45%",

                borderRadius: 6

            }

        },

        legend: {

            position: "top"

        },

        dataLabels: {

            enabled: false

        },

        yaxis: {

            labels: {

                formatter(value) {

                    return "Rp " + value.toLocaleString(
                        "id-ID"
                    );

                }

            }

        },

        tooltip: {

            y: {

                formatter(value) {

                    return "Rp " + value.toLocaleString(
                        "id-ID"
                    );

                }

            }

        }

    };

}
