import os
import requests

import pandas as pd
import numpy as np

from user_definition import *


def add_grade(access_token,
              course_id,
              quiz_id,
              submission_id,
              validation_token,
              questions_dict_value):
    """
    post a student's grade to the assignment
    https://canvas.instructure.com/doc/api/quiz_submissions.html#Manual+Scoring-appendix
    """
    url = f'https://usfca.instructure.com/api/v1/courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}'
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {access_token}'}
    body = '{"quiz_submissions": [{"attempt":1,"questions": ' + \
        questions_dict_value + '}]}'

    return requests.put(url, headers=headers, data=body)


def create_submission_id_for_students(course_id,
                                      quiz_id,
                                      access_token,
                                      per_page=100):
    """
    For adding grades and comments for quiz, we need user submission_id,
    which are unique to each submission.
    In your working directory, it will create {quiz_id}_submission_id_user.csv.

    Note : per_page - how many data/number of users to retrieve.
           If you have more than 100 students, increase this.
    """
    url = f'https://usfca.instructure.com/api/v1/courses/{course_id}/quizzes/{quiz_id}/submissions?per_page={per_page}'
    headers = {'Authorization': f'Bearer {access_token}'}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    submissions = data['quiz_submissions']
    pd_ids = pd.DataFrame()

    for data in submissions:
        id = data['id']
        quiz_id = data['quiz_id']
        user_id = data['user_id']
        validation_token = data['validation_token']
        pd_ids = pd.concat([pd_ids, pd.DataFrame(
            [id, quiz_id, user_id, validation_token]).transpose()])
    pd_ids.set_axis(["id", "quiz_id", "user_id",
                    "validation_token"], axis=1, inplace=True)
    pd_ids.to_csv(f"./{quiz_id}_submission_id_user.csv", index=False)
    return pd_ids


def create_gradebook_with_submission_id(access_token,
                                        course_id,
                                        quiz_id,
                                        file):
    """
    Return a panda dataframe, by merging {quiz_id}_submission_id_user.csv,
    and the file in the user_definition.py
    """
    pd_ids = create_submission_id_for_students(course_id,
                                               quiz_id,
                                               access_token)
    grade_book = pd.read_csv(file)
    grade_book.rename({'ID': 'user_id'}, axis=1, inplace=True)
    return pd.merge(pd_ids, grade_book, how='inner', on='user_id')


def check_questions(access_token, course_id, quiz_id):
    """
    This function returns the information of questions
    including question ids for the given quiz_id.
    """
    url = f'https://usfca.instructure.com/api/v1/courses/{course_id}/quizzes/{quiz_id}/questions?per_page=100'
    headers = {'Authorization': f'Bearer {access_token}'}
    resp = requests.get(url, headers=headers)


def main():
    gradebook = create_gradebook_with_submission_id(access_token,
                                                    course_id,
                                                    quiz_id,
                                                    file)
    for index, data in gradebook.iterrows():
        submission_id = data['id']
        validation_token = data['validation_token']
        question_dict_value = '{'
        for i in range(0, len(q_ids)):
            q_id = q_ids[i]
            q_grade_index = gradebook.columns.get_loc(q_ids[i])
            q_grade = data[q_grade_index]
            if i == len(q_ids) - 1:  # the last question
                q_grade_comments = data[q_grade_index + 1:].to_dict()
            else:
                next_q_grade_index = gradebook.columns.get_loc(q_ids[i+1])
                q_grade_comments = data[q_grade_index +
                                        1: next_q_grade_index].to_dict()

            if (i > 0):
                question_dict_value += ','
            question_dict_value += '\"' + str(q_id) + '\": {\"score\": \"' +\
                                   str(q_grade) + '\", \"comment\": \"' + \
                str(q_grade_comments) + '\"'

        question_dict_value += '}'
        add_grade(access_token,
                  course_id,
                  quiz_id,
                  submission_id,
                  validation_token,
                  question_dict_value)


if __name__ == '__main__':
    main()
