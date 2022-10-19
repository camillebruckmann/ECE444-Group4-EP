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
        conn = sqlite3.connect(db_file)
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

    for row in rows:
        print(row)

def select_course_by_faculty(conn, query): 
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses WHERE faculty = ?", (query,))
    rows = cur.fetchall()

    if not rows: 
        return("No results")

    for row in rows:
        print(row)

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


def main():
    database = r"ep_database"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query all courses")
        print(conn)
        select_all_courses(conn)
        print("2. Test")
        select_course_by_location(conn, 1)


if __name__ == '__main__':
    main()