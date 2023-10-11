# canvas_grading
Code for uploading assignment/quiz grades to Canvas for authorized instructors

## assignment_grading
This requires a file which is a csv file including ID, Total and comments.
- Required Environment Variables
    * ACCESS_TOKEN : You can create by following https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89
- Make sure to update user_definition.py to define course_id and assignment_id.
    * course_id and assignment_id is given in the Canvas assignment URL
    * EX. For https://usfca.instructure.com/courses/12345/assignments/67890, course id is 12345 and assignment id is 67890


## quiz_grading
This requires a file which is a csv file including ID, question_id and comments (if you have more questions to add scores it should have multiple question_id + comments/rubric columns).
<b> For each question_id, add the total score to appear on the question for the student </b>
- Required Environment Variables
    * ACCESS_TOKEN : You can create by following https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89
- Make sure to update user_definition.py to define course_id, assignment_id, and qustion_id list.
    * course_id and assignment_id is given in the Canvas assignment URL
    * EX. For https://usfca.instructure.com/courses/12345/assignments/67890, course id is 12345 and assignment id is 67890
    * You can find each question's id by using check_questions() or on the header of the exported file from "Student Analysis" on "Quiz Summary" 


## practicum_grading
This requires deadline_file, and contact_file to be defined in user_definition.py.
- deadline_file : a csv file including assignment_id and due_date. assignment_id is given in the Canvas assignment URL
    * EX. For https://usfca.instructure.com/courses/12345/assignments/67890, course id is 12345 and assignment id is 67890

- contact_file : a csv file including student name, id, sis user id, company name, faculty mentor name, faculty mentor email, company mentor names and emails. This will be used to send email to the student, faculty mentor and company mentors. 
    * <b>Canvas People</b> : On canvas, make sure to create a group for each company and assign the student (you can do this by uploading a csv file.). <b> Make sure that company name on the group and contact_file are the same and no space is added. </b>

- Required Environment Variables
    * ACCESS_TOKEN : You can create by following https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89
    * COURSE_ID : course_id in your canvas url.
    * SMTPUSER and SMTPPASS : Using @usfca.edu email SMTP, sending out reports to students and mentors. You can read https://support.google.com/a/answer/176600 to configure your GSuite settings.

- In order to automate the code, I'd encourage you to set something like Apache Airflow or Crontab.
    * Ex. 0 8 * * 1 source /home/dwoodbridge/.bash_profile; /usr/bin/python3 /home/dwoodbridge/practicum_weekly_report/practicum_weekly_report.py > /home/dwoodbridge/practicum_weekly_report/notes 2>&1