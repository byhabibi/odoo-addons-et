/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";


function isPlcPage() {
    return window.location.href.includes("action-492"); 
}


export class PlcHeader extends Component {
    setup() {
        this.state = useState({
            mp: "-",
            shift: "-"
        });

        this.loadData = async () => {
            try {
                const res = await rpc("/plc/latest", {});
                this.state.mp = res?.mp || "-";
                this.state.shift = res?.shift || "-";
            } catch (error) {
                console.error("PLC Header Error:", error);
            }
        };

        onMounted(() => {
            console.log("PLC HEADER MOUNTED ✅");

            if (!isPlcPage()) {
                console.log("Not PLC page ❌");
                return;
            }

            console.log("PLC PAGE DETECTED ✅");

            this.loadData();
            this.interval = setInterval(this.loadData, 5000);
        });
    }
}

PlcHeader.template = "plc_monitoring.PlcHeader";

registry.category("systray").add("plc_header", {
    Component: PlcHeader,
}, { sequence: 1 });


console.log("PLC HEADER JS LOADED 🚀");