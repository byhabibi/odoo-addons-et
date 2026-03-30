/** @odoo-module **/
import { Navbar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
const { onWillStart, useState } = owl;

patch(Navbar.prototype, "plc_monitoring.NavbarInfo", {
    setup() {
        this._super();
        this.rpc = useService("rpc");
        this.plcState = useState({ mp: "-", shift: "-" });

        onWillStart(async () => {
            await this._updatePlcInfo();
        });
    },

    async _updatePlcInfo() {
        const data = await this.rpc("/web/dataset/call_kw/plc.data/get_latest_info", {
            model: "plc.data",
            method: "get_latest_info",
            args: [],
            kwargs: {},
        });
        this.plcState.mp = data.mp;
        this.plcState.shift = data.shift;
    }
});