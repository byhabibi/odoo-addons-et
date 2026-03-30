/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, onMounted, useState, onWillUnmount } = owl;

export class PlcHeader extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({ mp: "-", shift: "-" });

        this.loadData = async () => {
            try {
                // Panggil langsung fungsi get_latest_info di model plc.data
                const res = await this.rpc("/web/dataset/call_kw/plc.data/get_latest_info", {
                    model: "plc.data",
                    method: "get_latest_info",
                    args: [],
                    kwargs: {},
                });
                this.state.mp = res?.mp || "-";
                this.state.shift = res?.shift || "-";
            } catch (error) {
                console.error("PLC Header Error:", error);
            }
        };

        onMounted(() => {
            // Kita jalankan loadData terus saja agar info MP & Shift 
            // selalu terlihat di navbar mana pun (Global)
            this.loadData();
            this.interval = setInterval(this.loadData, 5000); // Update tiap 5 detik
        });

        onWillUnmount(() => {
            if (this.interval) clearInterval(this.interval);
        });
    }
}

PlcHeader.template = "plc_monitoring.PlcHeader";

// Daftarkan ke systray (navbar kanan)
registry.category("systray").add("plc_header", {
    Component: PlcHeader,
}, { sequence: 1 });