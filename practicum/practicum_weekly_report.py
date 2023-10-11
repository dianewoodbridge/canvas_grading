from datetime import datetime
from datetime import date
from datetime import timedelta
import dateutil.parser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import pytz
import requests
import smtplib

import pandas as pd
import numpy as np

from user_definition import *


def check_graded(access_token,
                 course_id,
                 assignment_id,
                 user_id):
    """
    Check whether it has been graded.
    """
    url = f'https://usfca.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    submission = requests.get(url, headers=headers).json()
    grade = submission['grade']
    if grade is None:
        return False
    else:
        return True


def add_grade(access_token,
              course_id,
              assignment_id,
              user_id,
              grade,
              comment):
    """
    post a student's grade to the assignment
    """
    url = f'https://usfca.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    body = {'submission[posted_grade]': f'{grade}',
            'comment[text_comment]': f'{comment}'}
    return requests.put(url, headers=headers, data=body)


def check_late_submission(submission_time):
    """
    Returns True,
    if it was submitted after Sunday midnight.
    """
    tz = pytz.timezone('US/Pacific')
    yesterday = date.today() + timedelta(days=-1)
    today_local = datetime.combine(date.today(),
                                   datetime.min.time())
    today_utc = tz.localize(today_local,
                            is_dst=None)\
        .astimezone(pytz.utc)
    submission_time = dateutil.parser.isoparse(submission_time)

    return today_utc < submission_time


def retrieve_canvas_submission(access_token,
                               course_id,
                               assignment_id,
                               student_id):
    """
    retrieve submission and check
    whether it includes all the keywords.
    """
    # http request endpoint and headers
    url = f'https://usfca.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions?include[]=submission_history&per_page=100'
    headers = {'Authorization': f'Bearer {access_token}'}

    grade = 10  # whether it has all the keywords
    content = requests.get(url, headers=headers).json()
    comment = ''

    for answer in content:
        if answer['user_id'] == student_id:
            if answer['body'] is not None:
                # if None, it is not submitted.
                date = answer['submitted_at']
                user_id = answer['user_id']
                body = answer['body']

                for word in key_words:
                    if (word not in body.lower()):
                        print(f'{word}-{body.lower()}')
                        grade -= 1
                        comment += f'Missing Keyword : {word}\n'

                if check_late_submission(date):
                    grade = grade * 0.5
                    comment += 'Late submission\n'

                if check_graded(access_token,
                                course_id,
                                assignment_id,
                                user_id) in not True:  # Not graded
                    print(grade)
                    print(comment)
                    add_grade(access_token,
                              course_id,
                              assignment_id,
                              user_id,
                              grade,
                              comment)
                    return body

# DO NOT UNCOMMENT
#             else:
#                 user_id = answer['user_id']
#                 grade = 0
#                 comment = 'No submission\n'
#                 add_grade(access_token,
#                           course_id,
#                           assignment_id,
#                           user_id,
#                           grade,
#                           comment)

        # send email and grade


def retrieve_assignment_from_yesterday(deadline_file, student_id):
    """
    Retreive assignment due yesterday (midnight)
    """
    assignments = pd.read_csv(deadline_file)
    yesterday = date.today() + timedelta(days=-1)
    due_yesterday = assignments[assignments['due_date']
                                == yesterday.strftime('%m/%d/%y')]
    if len(due_yesterday):
        assignment_id = due_yesterday['assignment_id'].iloc[0]

        # retrieve answers
        return retrieve_canvas_submission(access_token,
                                          course_id,
                                          assignment_id,
                                          student_id)


def retrieve_contact_info(df):
    """
    Return student, faculty and company mentor info
    """
    student_names = df['Student'].unique()
    student_ids = df['ID'].unique()
    student_emails = df['SIS Login ID'].unique() + '@dons.usfca.edu'

    student_id_list = []
    to_list = []
    for i in range(0, len(student_names)):
        student_name = student_names[i].split(
            ', ')[1] + " " + student_names[i].split(', ')[0]
        to_list.append(student_name + ' <' + student_emails[i] + '>')
        student_id_list.append(student_ids[i])

    faculty_name = df['Faculty Mentor Name'].unique()
    faculty_email = df['Faculty Mentor Email'].unique()

    if not pd.isnull(faculty_name):
        to_list.append(faculty_name[0] + ' <' + faculty_email[0] + '>')

    mentor_name_1 = df['Company Mentor Name 1'].unique()
    mentor_email_1 = df['Company Mentor Email 1'].unique()

    if not pd.isnull(mentor_name_1):
        to_list.append(mentor_name_1[0] + ' <' + mentor_email_1[0] + '>')

    mentor_name_2 = df['Company Mentor Name 2'].unique()
    mentor_email_2 = df['Company Mentor Email 2'].unique()

    if not pd.isnull(mentor_name_2):
        to_list.append(mentor_name_2[0] + ' <' + mentor_email_2[0] + '>')

    mentor_name_3 = df['Company Mentor Name 3'].unique()
    mentor_email_3 = df['Company Mentor Email 3'].unique()
    if not pd.isnull(mentor_name_3):
        to_list.append(mentor_name_3[0] + ' <' + mentor_email_3[0] + '>')

    return (student_id_list, to_list)


def sendmail(sender, recipient, subject, text):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['Reply-To'] = sender
    msg['To'] = ", ".join(recipient)
    msg['Subject'] = subject
    print(msg['Subject'])

    part1 = MIMEText(text, 'html')
    msg.attach(part1)

    server = smtplib.SMTP_SSL(smtpserver)
    server.set_debuglevel(1)
    server.login(smtpuser, smtppass)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()


def create_email(company_name,
                 to_list,
                 body):
    """
    Create email updating reply-to and title and
    call sendmail()
    """
    sender = 'donotreply@datascience.usfca.edu'

    subject = f'{company_name} Internship Weekly Report'
    text = body

    sendmail(sender, to_list, subject, text)


def main():
    data = pd.read_csv(contact_file)
    company_list = sorted(list(data['Company Name'].dropna().unique()))

    for company in company_list:
        print("=========")
        company_info = data[data['Company Name'] == company]
        student_id_list, to_list = retrieve_contact_info(company_info)
        student_id = student_id_list[0]

        message = retrieve_assignment_from_yesterday(deadline_file, student_id)

        if message is not None:
            print(company)
            create_email(company,
                         to_list,
                         message)


if __name__ == '__main__':
    main()
