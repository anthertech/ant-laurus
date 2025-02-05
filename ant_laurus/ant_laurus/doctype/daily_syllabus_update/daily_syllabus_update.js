// Copyright (c) 2025, Hopeson and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Daily Syllabus Update", {
// 	refresh(frm) {

// 	},
// });
// frappe.ui.form.on('Daily Syllabus Update', {
//     course: function(frm) {
//         if (frm.doc.course) {
//             // Call the server script to fetch topics based on the selected course
//             frappe.call({
//                 method: "ant_laurus.ant_laurus.doctype.daily_syllabus_update.get_course_topics",  // Path to your server method
//                 args: {
//                     course_name: frm.doc.course  // Pass the selected course
//                 },
//                 callback: function(response) {
//                     if (response.message) {
//                         // Set the topic field options based on the topics retrieved from the server
//                         frm.set_df_property('topic', 'options', response.message);
//                         frm.set_value('topic', null);  // Clear previously selected topic
//                     }
//                 }
//             });
//         } else {
//             // Clear the topic field options if no course is selected
//             frm.set_df_property('topic', 'options', []);
//             frm.set_value('topic', null);
//         }
//     }
// });

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