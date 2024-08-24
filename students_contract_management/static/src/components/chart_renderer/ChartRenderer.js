/** @odoo-module **/
import {loadJS} from "@web/core/assets";
import {useService} from "@web/core/utils/hooks";

const {Component, onWillStart, useRef, onMounted, useEffect, onWillUnmount} = owl;

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart");
        this.actionService = useService("action");

        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");
            await loadJS("https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2");
        });

        useEffect(() => {
            this.renderChart();
        }, () => [this.props.config]);

        onMounted(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        const oldChartJS = document.querySelector("script[src='/web/static/lib/Chart/Chart.js']");
        if (oldChartJS) {
            return;
        }

        if (this.chart) {
            this.chart.destroy();
        }
        Chart.register(ChartDataLabels);
        this.chart = new Chart(
            this.chartRef.el,
            {
                type: this.props.type,
                data: this.props.config.data,
                options: {
                    responsive: true,
                    plugins: {

                        datalabels: {
                            formatter: (value, categories) => {

                                let sum = 0;
                                let dataArr = categories.chart.data.datasets[0].data;
                                dataArr.map(data => {
                                    sum += data;
                                });
                                return (value * 100 / sum).toFixed(2) + "%";


                            },
                            color: '#ffffff',
                            font: {
                                weight: 'bold',
                                size: 13,
                            },
                        },

                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                            text: this.props.title,
                            position: 'bottom',
                        }
                    },
                    scales: 'scales' in this.props.config ? this.props.config.scales : {},
                }
            }
        );
    }
}

ChartRenderer.template = "chartRenderer";
