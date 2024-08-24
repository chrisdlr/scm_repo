/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {browser} from "@web/core/browser/browser";
import {routeToUrl} from "@web/core/browser/router_service";
import {DateTimePicker} from "@web/core/datepicker/datepicker";
import {_t} from 'web.core';

const {Component, onWillStart, useState} = owl;
const {DateTime} = luxon;

// Custom imports and components
import {ChartRenderer} from "../chart_renderer/ChartRenderer";
import getRandomColor, {
    auxiliarColor,
    auxiliarColorSecondary,
    primaryBackgroundColors,
    secondaryBackgroundColors
} from "../graphicColors";

const PAYMENT_STATE = {
    "not_paid": _("Not paid"),
    "partially_paid": _("Partially paid"),
    "paid": _("Paid"),

}

export class StudentsContractDashboardGraphics extends Component {
    async setup() {
        this.state = useState({
            startDate: DateTime.local(),
            endDate: DateTime.local().plus({days: 7}),
            contractByPaymentState: {
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Total',
                        data: [],
                        backgroundColor: [],
                        hoverOffset: 10
                    }]
                },
            },
            contractByStudents: {
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Total',
                        data: [],
                        backgroundColor: [],
                        hoverOffset: 10
                    }]
                },
            },
            mostRequestedSubjects: {
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Total',
                        data: [],
                        backgroundColor: [],
                        hoverOffset: 10
                    }]
                },
            },
            mostRequestedTeachers: {
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Total',
                        data: [],
                        backgroundColor: [],
                        hoverOffset: 10
                    }]
                },
            },
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
        let domain = [
            ["create_date", ">=", this.state.startDate.toISO()],
            ["create_date", "<=", this.state.endDate.toISO()],
        ];

        let contractByPaymentState = {};
        let contractByStudents = {};
        let contractIds = [];
        const studentContractData = await this.orm.searchRead("students.contract", domain, ["payment_state", "student_id"], {order: "create_date asc"});
        if (studentContractData.length > 0) {
            for (const contract of studentContractData) {
                contractIds.push(contract.id);
                if (contract.payment_state) {
                    contractByPaymentState[PAYMENT_STATE[contract.payment_state]] = contractByPaymentState[PAYMENT_STATE[contract.payment_state]] ? contractByPaymentState[PAYMENT_STATE[contract.payment_state]] + 1 : 1;
                }

                if (contract.student_id) {
                    contractByStudents[contract.student_id[1]] = contractByStudents[contract.student_id[1]] ? contractByStudents[contract.student_id[1]] + 1 : 1;
                }
            }
        }

        const subjectsByContracts = await this.orm.searchRead("students.contract.lines", [["contract_id", "in", contractIds]], ["subject_id", "teacher_id"], {order: "create_date asc"});
        if (subjectsByContracts.length > 0) {
            let subjects = {};
            let teachers = {};
            for (const subject of subjectsByContracts) {
                if (subject.subject_id) {
                    subjects[subject.subject_id[1]] = subjects[subject.subject_id[1]] ? subjects[subject.subject_id[1]] + 1 : 1;
                }

                if (subject.teacher_id) {
                    teachers[subject.teacher_id[1]] = teachers[subject.teacher_id[1]] ? teachers[subject.teacher_id[1]] + 1 : 1;
                }
            }

            this.state.mostRequestedSubjects = {
                data: {
                    labels: Object.keys(subjects),
                    datasets: [{
                        label: 'Total',
                        data: Object.values(subjects),
                        backgroundColor: getRandomColor([auxiliarColor, primaryBackgroundColors], Object.keys(subjects).length),
                        hoverOffset: 10
                    }]
                },
                title: _t('Most requested subjects report'),
            }

            this.state.mostRequestedTeachers = {
                data: {
                    labels: Object.keys(teachers),
                    datasets: [{
                        label: 'Total',
                        data: Object.values(teachers),
                        backgroundColor: getRandomColor([secondaryBackgroundColors, primaryBackgroundColors], Object.keys(teachers).length),
                        hoverOffset: 10
                    }]
                },
            }
        }

        this.state.contractByPaymentState = {
            data: {
                labels: Object.keys(contractByPaymentState),
                datasets: [{
                    label: 'Total',
                    data: Object.values(contractByPaymentState),
                    backgroundColor: getRandomColor([auxiliarColorSecondary, primaryBackgroundColors], contractByPaymentState.length),
                    hoverOffset: 10
                }]
            },
            title: _t('Contracts by payment state report'),
        };

        this.state.contractByStudents = {
            data: {
                labels: Object.keys(contractByStudents),
                datasets: [{
                    label: 'Total',
                    data: Object.values(contractByStudents),
                    backgroundColor: getRandomColor([primaryBackgroundColors, secondaryBackgroundColors], Object.keys(contractByStudents).length),
                    hoverOffset: 10
                }]
            },
            title: _t('Contracts by students report'),
        }
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
