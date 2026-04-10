frappe.ui.form.on('Employee', {
    refresh: function(frm) {

        // remove all old buttons first
        frm.clear_custom_buttons();

        frm.add_custom_button('Mark Attendance', function() {

            //  prevent multiple clicks
            if (frm.attendance_clicked) return;
            frm.attendance_clicked = true;

            frappe.prompt([
                {
                    label: 'Status',
                    fieldname: 'status',
                    fieldtype: 'Select',
                    options: ['Present', 'Absent', 'Work From Home', 'Half Day'],
                    reqd: 1
                }
            ],
            function(values) {

                frappe.call({
                    method: 'attendance_app.api.mark_attendance',
                    args: {
                        employee: frm.doc.name,
                        status: values.status
                    },
                    callback: function(r) {

                        frappe.show_alert({
                            message: r.message,
                            indicator: 'green'
                        });

                        // reset click lock
                        frm.attendance_clicked = false;
                    },
                    error: function() {
                        frm.attendance_clicked = false;
                    }
                });

            }, 
            'Mark Attendance', 
            'Submit');

        });

    }
});