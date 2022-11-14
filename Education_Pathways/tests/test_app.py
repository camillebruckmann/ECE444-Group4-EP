from app import app
import sqlite3
import os
from minor import check_course_in_minor
from flask.testing import FlaskClient
from sqlite_config import create_connection, select_all_keywords_for_course, select_all_sessions, select_all_instructors
from sqlite3 import Error, connect

def test_check_course_in_minor():
    course = "MIE439H1S"
    minor = "Biomedical Engineering Minor"
    result = check_course_in_minor(course)

    assert result == minor


def test_user_register_endpoint():
    tester = app.test_client()
    response = tester.get("/user/register")

    assert response.status_code == 200

def test_user_login_endpoint():
    tester = app.test_client()
    response = tester.get("/user/login")

    assert response.status_code == 200

def test_search_endpoint():
    tester = app.test_client()
    response = tester.get("/search")

    assert response.status_code == 200

#Simrah 
def test_course_details():
    tester = app.test_client()
    response = tester.get("/courseDetails?code=ECE318H1")

    assert response.status_code == 200

#Simrah
def test_course_queries_reddit():
    tester = app.test_client() 
    response = tester.get("https://www.reddit.com/r/UofT/search/?q=ECE318&restrict_sr=1&sr_nsfw=&include_over_18=1")

    assert response.status_code == 200 

#Simrah 
def test_course_queries_uofthub():
    tester = app.test_client() 
    response = tester.get("https://uofthub.ca/course/ECE318")

    assert response.status_code == 200 

def test_course_graph_endpoint():
    tester = app.test_client()
    response = tester.get("/course/graph?code=ECE318H1")

    assert response.status_code == 200

def test_user_wishlist_endpoint():
    tester = app.test_client()
    response = tester.get("/user/wishlist")

    assert response.status_code == 200

def test_user_wishlist_addCourse_endpoint():
    tester = app.test_client()
    response = tester.get("/user/wishlist/addCourse")

    assert response.status_code == 200

def test_user_wishlist_removeCourse_endpoint():
    tester = app.test_client()
    response = tester.get("/user/wishlist/removeCourse")

    assert response.status_code == 200

def test_user_wishlist_minorCheck_endpoint():
    tester = app.test_client()
    response = tester.get("/user/wishlist/minorCheck")

    assert response.status_code == 200

def test_select_all_keywords_for_course():
    database = r"ep_database"

    # create a database connection
    conn = create_connection(database)
    assert(select_all_keywords_for_course(conn, 'ECE444') == ['Software Engineer', 'Full Stack Developer', 'Database Administrator', 'Site Reliability Engineer', 'DevOps Engineer'])

def test_select_all_sessions():
    database = r"ep_database"
    
    conn = create_connection(database)

    assert(select_all_sessions(conn) == [(1, 2022, None, 1, 'ECE444', 1, 0, 1), (2, 2022, None, 1, 'CSC384', 1, 0, 1), (3, 2022, None, 1, 'ECE496', 3, 0, 1), (4, 2022, None, 3, 'ECE496', 1, 0, 1), (5, 2022, None, 1, 'PHL233', 1, 0, 1), (6, 2022, None, 1, 'POL101', 1, 0, 0), (7, 2022, None, 2, 'ECE318', 1, 0, 1), (8, 2022, None, 2, 'ECE368', 1, 0, 1), (9, 2022, None, 2, 'ECE568', 1, 0, 1), (10, 2022, None, 2, 'TEP445', 1, 0, 1), (11, 2022, None, 2, 'ECE311', 1, 0, 1), (12, 2022, None, 2, 
'ECE344', 1, 0, 1), (13, 2022, None, 2, 'ECE421', 1, 0, 1), (14, 2022, None, 2, 'ECE472', 1, 0, 1), (15, 2022, None, 1, 'ECE302', 1, 0, 0), (16, 2022, None, 1, 'ECE326', 1, 0, 1), (17, 2022, None, 1, 'ECE345', 1, 0, 1), (18, 2022, None, 1, 'ECE361', 1, 0, 1), (19, 2022, None, 1, 'APS360', 1, 0, 0), (20, 2022, None, 1, 'TEP444', 1, 0, 1)])

def test_select_all_instructors():
    database = r"ep_database"
 
    conn = create_connection(database)

    assert(select_all_instructors(conn) == [(1, 'Shurui Zhou', 'shuruiz@ece.utoronto.ca'), (2, 'Steve Engels', 'csc384-2022-09@cs.toronto.edu'), (3, 'Courtney Jung', 'courtney.jung@utoronto.ca'), (4, 'Imogen Dickie', 'imogen.dickie@utoronto.ca'), (5, 'Belinda Wang', 'belinda.wang@utoronto.ca'), (6, 'Khoman Phang', 'khoman.phang@utoronto.ca'), (7, 'Bruno Korst', 'bkf@ece.utoronto.ca')])