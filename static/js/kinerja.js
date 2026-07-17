function initKinerjaGauge() {

    const container = document.getElementById(
        "kinerjaGauge"
    );

    if (!container) {
        return;
    }

    const chart = JSON.parse(
        container.dataset.chart
    );

    const data = getKinerjaData(
        chart
    );

    const options = buildKinerjaGauge(
        data
    );

    renderChart(
        container,
        options
    );

}

function getKinerjaData(chart) {

    return {

        persentase: chart.persentase,

        target: chart.target,

        realisasi: chart.realisasi,

        satuan: chart.satuan

    };

}

function buildKinerjaGauge(data) {

    return {

        chart: {

            type: "radialBar",

            height: 340,

            toolbar: {

                show: false

            }

        },

        series: [

            data.persentase

        ],

        labels: [

            "Capaian"

        ],

        plotOptions: {

            radialBar: {

                hollow: {

                    size: "72%"

                },

                dataLabels: {

                    name: {

                        fontSize: "18px",

                        offsetY: 24

                    },

                    value: {

                        fontSize: "42px",

                        fontWeight: 700,

                        offsetY: -10,

                        formatter(value) {

                            return Number(value).toFixed(0) + "%";

                        }

                    }

                }

            }

        },

        stroke: {

            lineCap: "round"

        }

    };

}
