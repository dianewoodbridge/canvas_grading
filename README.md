# canvas_grading
Code for uploading assignment/quiz grades to Canvas for authorized instructors

## practicum_grading
This requires deadline_file, and contact_file to be defined in user_definition.py.
- deadline_file : a csv file including assignment_id and due_date. assignment_id is given in the Canvas assignment URL
* EX. For https://usfca.instructure.com/courses/12345/assignments/67890, course id is 12345 and assignment id is 67890

- contact_file : a csv file including student name, id, sis user id, company name, faculty mentor name, faculty mentor email, company mentor names and emails. This will be used to send email to the student, faculty mentor and company mentors.

- Required Environment Variables
-- ACCESS_TOKEN : You can create by following https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89
-- COURSE_ID : course_id in your canvas url.
-- SMTPUSER and SMTPPASS : Using @usfca.edu email SMTP, sending out reports to students and mentors. You can read https://support.google.com/a/answer/176600 to configure your GSuite settings.
