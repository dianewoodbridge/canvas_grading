import requests
import os

import pandas as pd
import numpy as np

from user_definition import *


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
    print(url)
    headers = {'Authorization': f'Bearer {access_token}'}
    body = {'submission[posted_grade]': f'{grade}',
            'comment[text_comment]': f'{comment}'}
    return requests.put(url, headers=headers, data=body)


def main():
    table = pd.read_csv(file)
    for index, data in table.iterrows():
        user_id = int(data['ID'])
        grade = data['Total']
        comment = data.to_dict()

        add_grade(access_token,
                  course_id,
                  assignment_id,
                  user_id,
                  grade,
                  comment)


if __name__ == '__main__':
    main()
