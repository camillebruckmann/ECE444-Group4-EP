import sqlite3

conn = sqlite3.connect('ep_database') 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS Courses
          ([course_code] TEXT PRIMARY KEY,
           [course_name] TEXT, 
           [faculty] TEXT CHECK ( faculty IN ('Engineering', 'Arts & Science'))
           )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS Sessions
          ([session_id] INTEGER PRIMARY KEY, 
          [year] INTEGER, [semester] INTEGER, 
          [section] INTEGER, 
          [course_code] INTEGER, 
          [campus] INTEGER, 
          [delivery] INTEGER, 
          [synchronous] INTEGER, 
          FOREIGN KEY(course_code) REFERENCES Courses(course_code)
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS Keywords
          ([keyword] INTEGER,
           [course_code] TEXT, 
           PRIMARY KEY(keyword, course_code)
           )
          ''')


c.execute('''
          CREATE TABLE IF NOT EXISTS Instructors
          ([instructor_id] INTEGER PRIMARY KEY,
           [full_name] TEXT, 
           [email] TEXT
           )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS TAs
          ([ta_id] INTEGER PRIMARY KEY,
           [full_name] TEXT, 
           [email] TEXT
           )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS instructor_sessions
          ([session_id] INTEGER,
           [instructor_id] INTEGER, 
           FOREIGN KEY(session_id) REFERENCES Sessions(session_id),
           FOREIGN KEY(instructor_id) REFERENCES Instructors(instructor_id),
           PRIMARY KEY(session_id, instructor_id)
           )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS ta_sessions
          ([session_id] INTEGER,
           [ta_id] INTEGER, 
           FOREIGN KEY(session_id) REFERENCES Sessions(session_id),
           FOREIGN KEY(ta_id) REFERENCES TAs(ta_id),
           PRIMARY KEY(session_id, ta_id)
           )
          ''')
                     
conn.commit()