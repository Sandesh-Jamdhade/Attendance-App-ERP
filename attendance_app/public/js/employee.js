frappe.ui.form.on('Employee', {
    refresh: function(frm) {

        frm.add_custom_button('Mark Attendance', function() {

            frappe.call({
                method: 'attendance_app.api.mark_attendance',
                args: {
                    employee: frm.doc.name,
                    status: 'Present'
                },
                callback: function(r) {

                    // Silent success
                    frappe.show_alert({
                        message: "Attendance Updated",
                        indicator: 'green'
                    });

                }
            });

        });

    }
});