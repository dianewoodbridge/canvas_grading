import os


#  input files required to generate emails on time
deadline_file =  # ADD ABSOULTE PATH FOR assignment_deadline.csv
contact_file =   # ADD ABSOULTE PATH FOR Company_Student_Mentor_Assignment.csv

smtpserver = 'smtp.gmail.com:465'

# required keywords in the submission
key_words = ['practicum name',
             'week of (start date of the week)',
             'student names',
             'hours / days worked, location worked',
             'company meeting date',
             'weekly faculty meeting date',
             'previous weeks objectives',
             'what i/we achieved this week',
             'the objective for next week']

access_token = os.getenv('ACCESS_TOKEN')
course_id = os.getenv('COURSE_ID')
smtpuser = os.getenv('SMTPUSER')
smtppass = os.getenv('SMTPPASS')
