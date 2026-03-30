/** @odoo-module **/

setInterval(() => {
    const url = window.location.href;

    // hanya jalan di PLC page
    if (url.includes("action-492")) {
        console.log("AUTO REFRESH PLC 🔄");
        location.reload();
    }
}, 5000)