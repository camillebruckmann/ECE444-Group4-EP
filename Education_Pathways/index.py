# this is the flask core

from flask import Flask, send_from_directory, jsonify, request
from flask_restful import Api,Resource, reqparse
import os

import pandas as pd
df = pd.read_csv("resources/courses.csv")

filters = {"Term": [], "Campus": [], "Division":[]}

import config
app = Flask(__name__, static_folder='frontend/build')
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# MongoDB URI
DB_URI = "mongodb+srv://Cansin:cv190499@a-star.roe6s.mongodb.net/A-Star?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

config.init_app(app)
config.init_db(app)
config.init_cors(app)

database = r"ep_database"
import sqlite_config
conn = sqlite_config.create_connection(database)


# route functions
def search_course_by_code(s):
    # return all the courses whose course code contains the str s
    
    course_ids = df[df['Code'].str.contains(s.upper())].index.tolist()
    if len(course_ids) == 0:
        return []
    if len(course_ids) > 10:
        course_ids = course_ids[:10]
    res = []
    for i, course_id in enumerate(course_ids):
        d = df.iloc[course_id].to_dict()
        pre_req_processed = d['Pre-requisites'].strip('][').replace("'", '')
        res_d = {
            '_id': i,
            'code': d['Code'],
            'name': d['Name'],
            'description': d['Course Description'],
            'prereq': pre_req_processed,
            'coreq': ['APS102H1, ECE102H1'],
            'exclusion': ['APS102H1, ECE102H1'],
            'division': d['Division'],
            'department': d['Department']
        }
        res.append(res_d)
    return res

def search_n_filter(s, filters):
    course_id = df[df['Code'].str.contains(s.upper())]
    for key,values in filters.items():
        if (len(values) != 0):
            for val in values:
                course_id = course_id[course_id[key].str.contains(val)]
            
    course_ids = course_id.index.tolist()
    if len(course_ids) == 0:
        return []
    if len(course_ids) > 10:
        course_ids = course_ids[:10]
    res = []
    for i, course_id in enumerate(course_ids):
        d = df.iloc[course_id].to_dict()
        pre_req_processed = d['Pre-requisites'].strip('][').replace("'", '')
        res_d = {
            '_id': i,
            'code': d['Code'],
            'name': d['Name'],
            'description': d['Course Description'],
            'prereq': pre_req_processed,
            'coreq': ['APS102H1, ECE102H1'],
            'exclusion': ['APS102H1, ECE102H1'],
            'division': d['Division'],
            'department': d['Department']
        }
        res.append(res_d)
    return res

def create_filter(req):
    fall = req.values['fall']
    winter = req.values['winter']
    summer = req.values['summer']
    stgeorge = req.values['stgeorge']
    mississauga = req.values['mississauga']
    scarborough = req.values['scarborough']
    music = req.values['music']
    eng = req.values['eng']
    arts = req.values['arts']
    architecture = req.values['architecture']

    if (fall != ""):
        filters['Term'].append(fall)
    if (winter != ""):
        filters['Term'].append(winter)
    if (summer != ""):
        filters['Term'].append(summer)
    if (stgeorge != ""):
        filters['Campus'].append(stgeorge)
    if (mississauga != ""):
        filters['Campus'].append(mississauga)
    if (scarborough != ""):
        filters['Campus'].append(scarborough)
    if (music != ""):
        filters['Division'].append(music)
    if (eng != ""):
        filters['Division'].append(eng)
    if (arts != ""):
        filters['Division'].append(arts)
    if (architecture != ""):
        filters['Division'].append(architecture)


class SearchCourse(Resource):
    def get(self):
        filters["Term"] = []
        filters["Campus"] = []
        filters["Division"] = []
        input = request.args.get('input')
        create_filter(request)
        print(filters)
        courses = search_n_filter(input,filters)

        if len(courses) > 0:
            try:
                resp = jsonify(courses)
                resp.status_code = 200
                filters["Term"] = []
                filters["Campus"] = []
                filters["Division"] = []
                return resp
            except Exception as e:
                resp = jsonify({'error': str(e)})
                resp.status_code = 400
                filters["Term"] = []
                filters["Campus"] = []
                filters["Division"] = []
                return resp

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('input', required=True)
        data = parser.parse_args()
        input = data['input']
        courses = search_course_by_code(input)
        if len(courses) > 0:
            try:
                resp = jsonify(courses)
                resp.status_code = 200
                return resp
            except Exception as e:
                resp = jsonify({'error': 'something went wrong'})
                resp.status_code = 400
                return resp

class ShowCourse(Resource):
    def get(self):
        code = request.args.get('code')
        courses = search_course_by_code(code)
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {code} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 400
            return resp
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True)
        data = parser.parse_args()
        code = data['code']
        courses = search_course_by_code(code)
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {code} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 400
            return resp


def query_to_paragraph(query_result):
    paragraph = ""

    if (len(query_result) > 0):
        paragraph = query_result[0]
    if (len(query_result) > 1):
        for result in query_result[1:]:
            paragraph += ", " + result

    return paragraph


# API Endpoints
rest_api = Api(app)
# rest_api.add_resource(controller.SearchCourse, '/searchc')
rest_api.add_resource(SearchCourse, '/searchc')
# rest_api.add_resource(controller.ShowCourse, '/course/details')
rest_api.add_resource(ShowCourse, '/course/details')

# API Endpoints
import controller
api = Api(app)
api.add_resource(controller.UserRegistration, '/user/register')
api.add_resource(controller.UserLogin, '/user/login')

# api.add_resource(controller.SearchCourse, '/searchc')
# api.add_resource(controller.ShowCourse, '/course/details')
api.add_resource(controller.ShowCourseGraph, '/course/graph')

api.add_resource(controller.UserWishlist, '/user/wishlist')
api.add_resource(controller.UserWishlistAdd, '/user/wishlist/addCourse')
api.add_resource(controller.UserWishlistRemove, '/user/wishlist/removeCourse')
api.add_resource(controller.UserWishlistMinorCheck, '/user/wishlist/minorCheck')

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/<code>/course_info", methods=["GET"])
def getCourseInfo(code):
    code = code.upper()
    with conn:       
        name = sqlite_config.select_coursename_for_course(conn, code)
        desc = sqlite_config.select_description_for_course(conn, code)
        keywords = sqlite_config.select_all_keywords_for_course(conn, code)
        prereq_query_result = sqlite_config.select_all_prerequisites_for_course(conn, code)
        coreq_query_result = sqlite_config.select_all_corequisites_for_course(conn, code)
        exclusions_query_result = sqlite_config.select_all_exclusions_for_course(conn, code)

    name = name[0]
    desc = desc[0][0]
    keywords = query_to_paragraph(keywords)
    prereqs_list = query_to_paragraph(prereq_query_result)
    coreqs_list = query_to_paragraph(coreq_query_result)
    exclusions_list = query_to_paragraph(exclusions_query_result)

    info = ({
            "course_code": code,
            "name": name,
            "description": desc,
            "keywords": keywords,
            "prereqs": prereqs_list,
            "coreqs": coreqs_list,
            "exclusions": exclusions_list
    })
    info = jsonify(info)

    return info

@app.route("/<code>/prof", methods=["GET"])
def getProfessors(code):
    code = code.upper()
    with conn:
        query_result = sqlite_config.select_professors_by_course(conn, code)
    profs_list = query_to_paragraph(query_result)
    prof = ({"profs": profs_list})
    prof = jsonify(prof)

    return prof
    
@app.route("/<code>/careers", methods=["GET"])
def getCareers(code):
    code = code.upper()
    with conn:
        query_result = sqlite_config.select_all_careers_for_course(conn, code)
    careers_list = query_to_paragraph(query_result)
    careers = ({"careers": careers_list})
    careers = jsonify(careers)

    return careers

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, extra_files=['app.py', 'controller.py', 'model.py'])
    app.run(threaded=True, port=5000)

    # with open("test.json") as f:
    #     data = json.load(f)
    # for i in range(75):
    #     i = str(i)
    #     Course(name=data["name"][i], code=data["code"][i], description=data["description"][i], prereq=data["prereq"][i], coreq=data["coreq"][i], exclusion=data["exclusion"][i]).save()

    
    
