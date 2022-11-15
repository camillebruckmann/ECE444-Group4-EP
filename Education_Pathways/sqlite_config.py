import sqlite3
from sqlite3 import Error, connect

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
    except Error as e:
        print(e)

    return conn


def select_all_courses(conn):
    """
    EXAMPLE QUERY
    Query all rows in the courses table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses")

    rows = cur.fetchall()

    return rows

def select_course(conn, query):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses WHERE course_code = ?", (query,))
    rows = cur.fetchall()
    rows.append(select_all_prerequisites_for_course(conn, query))
    rows.append(select_all_corequisites_for_course(conn, query))
    rows.append(select_all_exclusions_for_course(conn, query))

    if not rows: 
        return("No results")

    return rows

def select_coursename_for_course(conn, query):
    cur = conn.cursor()
    cur.execute("SELECT Courses.course_name FROM Courses WHERE course_code = ?", (query,))
    rows = cur.fetchall()

    if not rows: 
        return("No results")

    return rows

def select_description_for_course(conn, query):
    cur = conn.cursor()
    cur.execute("SELECT Courses.course_description FROM Courses WHERE course_code = ?", (query,))
    rows = cur.fetchall()

    if not rows: 
        return("No results")

    return rows


def select_course_by_faculty(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses WHERE faculty = ?", (query,))
    rows = cur.fetchall()

    if not rows: 
        return("No results")

    return rows

#Queries: 0 = N/A, 1 = St. George, 2 = Missisauga, 3 = Scarborough
def select_course_by_location(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT Courses.course_code, course_name, faculty \
                FROM Courses \
                INNER JOIN Sessions \
                ON Courses.course_code = Sessions.course_code \
                WHERE campus = ?", (query,))
    rows = cur.fetchall()

    if not rows: 
        return("No results")

    return rows

#Queries: 0 = In Person, 1 = Online
def select_course_by_delivery(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT Courses.course_code, course_name, faculty \
                FROM Courses \
                INNER JOIN Sessions \
                ON Courses.course_code = Sessions.course_code \
                WHERE delivery = ?", (query,))
    rows = cur.fetchall()

    if not rows: 
        return("No results")

    return rows

def select_professor_by_course_session_id(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * from Instructors \
                WHERE instructor_id = (SELECT instructor_id FROM \
                instructor_sessions WHERE session_id = ?)", (query,))
    rows = cur.fetchall()
    return rows

def select_professors_by_course(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * from Sessions \
                WHERE course_code = ?", (query,))
    rows = cur.fetchall()
    profs = []
    for row in rows:
        instructors = select_professor_by_course_session_id(conn, row[0])
        for i in instructors:
            profs.append(i[1])
    return profs

def select_all_prerequisites_for_course(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * from Courses \
                WHERE course_code = (SELECT prerequisite_course_code FROM \
                Prerequisites WHERE course_code = ?)", (query,))
    rows = cur.fetchall()
    list = []
    if (len(rows) > 0) :
        for course in rows:
            if (len(course) > 0):
                list.append(course[0])
    return list

def select_all_corequisites_for_course(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * from Courses \
                WHERE course_code = (SELECT corequisite_course_code FROM \
                Corequisites WHERE course_code = ?)", (query,))
    rows = cur.fetchall()
    list = []
    if (len(rows) > 0) :
        for course in rows:
            if (len(course) > 0):
                list.append(course[0])
    return list

def select_all_exclusions_for_course(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * from Courses \
                WHERE course_code = (SELECT exclusion_course_code FROM \
                Exclusions WHERE course_code = ?)", (query,))
    rows = cur.fetchall()
    list = []
    if (len(rows) > 0) :
        for course in rows:
            if (len(course) > 0):
                list.append(course[0])
    return list

# In this case, keywords for a course and related careers are synonymous
def select_all_keywords_for_course(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * FROM Keywords WHERE course_code = ?", (query,))
    rows = cur.fetchall()

    keywords = []
    for row in rows:
        keywords.append(row[0])
    
    return keywords


def select_all_sessions(conn): 
    cur = conn.cursor()
    cur.execute("SELECT * FROM Sessions")
    rows = cur.fetchall()
    return rows

def select_all_instructor_sessions(conn): 
    cur = conn.cursor()
    cur.execute("SELECT * FROM instructor_sessions")
    rows = cur.fetchall()
    return rows

def select_all_instructors(conn): 
    cur = conn.cursor()
    cur.execute("SELECT * FROM Instructors")
    rows = cur.fetchall()
    return rows

#For testing purposes
def main():
    database = r"ep_database"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query all courses")
        print(select_all_keywords_for_course(conn, 'ECE444'))
        print("2. Test")
        print('2')
        print(select_all_sessions(conn))
        print('4')
        print(select_all_instructors(conn))
        print('5')
        print(select_all_courses(conn))
        print(select_professor_by_course_session_id(conn, 1))
        print('6')
        select_course_by_location(conn, 1)
        # print(select_course(conn, 'ECE444'))
        # print(select_description_for_course(conn, 'ECE444')[0][0])


if __name__ == '__main__':
    main()