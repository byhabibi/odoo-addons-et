/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks"; // Odoo 16 pakai hooks untuk RPC
const { Component, onMounted, useState, onWillUnmount } = owl; // Ambil langsung dari global owl

function isPlcPage() {
    // Tips: Jangan cuma cek 'action-492' karena ID action bisa berubah di DB berbeda.
    // Tapi untuk sementara ini tetap saya biarkan sesuai logika kamu.
    return window.location.href.includes("action-492"); 
}

export class PlcHeader extends Component {
    setup() {
        this.rpc = useService("rpc"); // Cara Odoo 16 panggil RPC service
        this.state = useState({
            mp: "-",
            shift: "-"
        });

        this.loadData = async () => {
            try {
                // Di Odoo 16, rpc service dipanggil seperti ini
                const res = await this.rpc("/plc/latest"); 
                this.state.mp = res?.mp || "-";
                this.state.shift = res?.shift || "-";
            } catch (error) {
                console.error("PLC Header Error:", error);
            }
        };

        onMounted(() => {
            console.log("PLC HEADER MOUNTED ✅");
            if (isPlcPage()) {
                console.log("PLC PAGE DETECTED ✅");
                this.loadData();
                this.interval = setInterval(this.loadData, 5000);
            }
        });

        // PENTING: Di Odoo 16, bersihkan interval agar tidak memory leak
        onWillUnmount(() => {
            if (this.interval) {
                clearInterval(this.interval);
            }
        });
    }
}

PlcHeader.template = "plc_monitoring.PlcHeader";

// Daftarkan ke systray (navbar kanan)
registry.category("systray").add("plc_header", {
    Component: PlcHeader,
}, { sequence: 1 });