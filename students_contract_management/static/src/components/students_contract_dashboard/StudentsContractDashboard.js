/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {browser} from "@web/core/browser/browser";
import {routeToUrl} from "@web/core/browser/router_service";
import {DateTimePicker} from "@web/core/datepicker/datepicker";

const {Component, onWillStart, useState} = owl;
const {DateTime} = luxon;

// Custom imports and components
import {ChartRenderer} from "../chart_renderer/ChartRenderer";


export class StudentsContractDashboardGraphics extends Component {
    async setup() {
        this.state = useState({
            startDate: DateTime.local(),
            endDate: DateTime.local().plus({days: 7}),
            discountRules: [],
            discountsByContract: [],
            discountsByStudent: [],
        });

        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.actionService = useService("action");

        const oldChartJS = document.querySelector("script[src='/web/static/lib/Chart/Chart.js']");
        const router = useService("router");

        if (oldChartJS) {
            let {search, hash} = router.current;
            search.oldChartJS = oldChartJS.src !== null ? "0" : "1";
            let actionViewId = await this.orm.searchRead("ir.actions.actions", [["name", "=", "Discounts Dashboard Graphics"]], ["id"]);
            hash.action = actionViewId[0].id;
            browser.location.href = browser.location.origin + routeToUrl(router.current);
            browser.location.reload();
        }

        onWillStart(async () => {
            await this.getDates();
            await this.getDashboardData();
        });
    }

    async getDashboardData() {
        // TODO: GETTERS
    }

    async onDateChange(datetime, dateType) {
        if (dateType === "startDate") {
            this.state.startDate = datetime || false;
        }

        if (dateType === "endDate") {
            this.state.endDate = datetime || false;
        }

        await this.getDashboardData();
    }

    async onChangePeriod() {
        await this.getDates();
        await this.getDashboardData();
    }

    async getDates() {
        this.state.current_date = moment().format('YYYY-MM-DD');
        this.state.previous_date = moment().subtract(this.state.period, 'days').format('YYYY-MM-DD');
    }

}

StudentsContractDashboardGraphics.template = "StudentsContractDashboardGraphics";
StudentsContractDashboardGraphics.components = {ChartRenderer, DateTimePicker};

registry.category("actions").add("students_contract_dashboard", StudentsContractDashboardGraphics);
