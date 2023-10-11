access_token = os.getenv('ACCESS_TOKEN')

file =  # .csv file with question grades and comments. Ex. "2023_MSDS691_Quiz2_Grading-FINAL.csv"
course_id =  # course id in string. Ex. '1614565'
quiz_id =   #  quiz id in string. Ex. '2431502', you can find it at the end of the URL on your quiz : https://usfca.instructure.com/courses/1614565/quizzes/2431502
q_ids =  # A list of question id strings. ['47493561', '47493560', '47493562'], you can find them on the header of the exported file from "Student Analysis" on "Quiz Summary" 