import sqlite3

conn = sqlite3.connect('ep_database') 
c = conn.cursor()

# Adding keywords for course ECE444
c.execute(''' INSERT INTO Keywords(keyword,course_code)
              VALUES("DevOps Engineer", "ECE444") ''')


conn.commit()