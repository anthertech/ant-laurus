// Copyright (c) 2025, Hopeson and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Syllabus Update', {
    course: function(frm) {
        if (frm.doc.course) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Course',
                    name: frm.doc.course
                },
                callback: function(r) {
                    if (r.message) {
                        console.log(r.message, "this is message................................");
                        let topics = r.message.topics || [];
                        let topic_list = topics.map(topic => topic.topic);

                        frm.set_query('topic', function() {
                            return {
                                filters: {
                                    name: ['in', topic_list]
                                },
                                // Remove the default limit by setting a high page length
                                page_length: 1000 // Adjust this as needed to fit your data
                            };
                        });

                        frm.refresh_field('topic');
                    }
                }
            });
        }
    }
});