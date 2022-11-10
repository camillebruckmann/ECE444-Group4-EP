from app import app
from minor import check_course_in_minor
from flask.testing import FlaskClient



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

