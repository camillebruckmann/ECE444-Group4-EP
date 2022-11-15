import React, { Component } from 'react';
import './css/course-description.css'
import 'bootstrap/dist/css/bootstrap.css';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import requisite_label from './img/requisite-label.png'
import empty_star from './img/star.png'
import API from '../api';
import starred from './img/starred.png'
import axios from "axios"

let star = empty_star;

class CourseDescriptionPage extends Component {

  constructor(props){
    super(props)

    this.state = {
      course_code: "",
      course_name: "",
      division: "Faculty of Applied Science and Engineering",
      department: "Department of Edward S. Rogers Sr. Dept. of Electrical & Computer Engineering",
      graph : "",
      course_description: "",
      syllabus: "",
      redditpeerfeedback: "",
      uofthubfeedback: "",
      professor: "",
      relatedcareers: "",
      prerequisites: "",
      corequisites: "",
      exclusions: "",
      starred: false,
      graphics: [],
      username: localStorage.getItem('username')
    }
  }



  componentDidMount() {
  // console.log("pass in course code: ", this.props.match.params.code)
    // API.get(`/course/details?code=${this.props.match.params.code}`, {
    //   code: this.props.course_code
    // })
    axios.get(`https://assignment-1-starter-template.herokuapp.com/course/details?code=${this.props.match.params.code}`, {
      code: this.props.course_code 
    })
      .then(res => {
        
        this.setState({graph: res.data.course.graph})
        
        let temp_graph = []
        //temp_graph.push(<ShowGraph graph_src={this.state.graph}></ShowGraph>)
        this.setState({graphics: temp_graph})

    })

    let full_course_code = this.props.match.params.code
    let short_course_code = full_course_code.slice(0, -2)

    fetch("http://localhost:5000/"+short_course_code+"/course_info").then(response =>
      response.json().then(info =>{
        this.setState({course_code: info.course_code})
        this.setState({course_name: info.name})
        this.setState({course_description: info.description})
        this.setState({keywords: info.keywords})
        this.setState({prerequisites: info.prereqs})
        this.setState({corequisites: info.coreqs})
        this.setState({exclusions: info.exclusions})
      }));

    let syllabus_link = "http://courses.skule.ca/course/" + this.props.match.params.code
    this.setState({syllabus : syllabus_link})

    let uofthubpeerfeedback_link = "http://uofthub.ca/course/" + this.props.match.params.code.slice(0,6)
    this.setState({uofthubfeedback : uofthubpeerfeedback_link})

    let peerfeedback_link = "http://www.reddit.com/r/UofT/search/?q=" + this.props.match.params.code.slice(0,6) + "&restrict_sr=1&sr_nsfw=&include_over_18=1" 
    this.setState({redditpeerfeedback : peerfeedback_link})

    fetch("http://localhost:5000/"+short_course_code+"/prof").then(response =>
      response.json().then(prof =>{
        this.setState({professor: prof.profs})
      }));

    fetch("http://localhost:5000/"+short_course_code+"/careers").then(response =>
    response.json().then(careers =>{
      this.setState({relatedcareers: careers.careers})
    }));

  }


  openLink = () => {
    const newWindow = window.open(this.state.syllabus, '_blacnk', 'noopener,noreferrer');
    if (newWindow) {
      newWindow.opener = null;
    }
  }

  openLinkPeer = () => {
    const newWindow = window.open(this.state.redditpeerfeedback, '_blacnk', 'noopener,noreferrer');
    if (newWindow) {
      newWindow.opener = null;
    }
  }

  openLinkPeerUofTHub = () => {
    const newWindow = window.open(this.state.uofthubfeedback, '_blacnk', 'noopener,noreferrer');
    if (newWindow) {
      newWindow.opener = null;
    }
  }


	render() {
		return(

      <div className="page-content">
        <Container className="course-template">
          <Row float="center" className="course-title">
            <Col xs={8}>
              <h1>{this.state.course_code} : {this.state.course_name}</h1>
            </Col>
            {/* <Col xs={4}>
              <img src={star} onClick={this.check_star} alt="" />
            </Col> */}
          </Row>
          <Row>
            <Col className="col-item">
              <h3>Division</h3>
              <p>{this.state.division}</p>
            </Col>
            <Col className="col-item">
              <h3>Department</h3>
              <p>{this.state.department}</p>
            </Col>
            <Col className="col-item">
              <h3>Past Tests and Syllabi</h3>
              <button className={"syllabus-link"} onClick={this.openLink}>View</button>
            </Col>
            <Col className="col-item">
              <h3>Course Queries on Reddit</h3>
              <button className={"peerfeedback-link"} onClick={this.openLinkPeer}>View</button>
            </Col>
            <Col className="col-item">
              <h3>Course Reviews on UofTHub.ca</h3>
              <button className={"uofthubpeerfeedback-link"} onClick={this.openLinkPeerUofTHub}>View</button>
            </Col>
          </Row>
          <Row className="col-item course-description">
            <h3>Course Description</h3>
            <p>{this.state.course_description}</p>
          </Row>
          <Row className="col-item course-professor">
            <h3>Course Professor</h3>
            <p>{this.state.professor}</p>
          </Row>
          <Row className="col-item course-relatedcareers">
            <h3>Related Careers</h3>
            <p>{this.state.relatedcareers}</p>
          </Row>
          <Row className="col-item course-requisite">
            <Row>
              <h3>Course Requisites</h3>
            </Row>
            <Row>
              <Col className="requisites-display">
                <h4>Pre-Requisites</h4>
                <p>{this.state.prerequisites}</p>
              </Col>
              <Col className="requisites-display">
                <h4>Co-Requisites</h4>
                <p>{this.state.corequisites}</p>
              </Col>
              <Col className="requisites-display">
                <h4>Exclusion</h4>
                <p>{this.state.exclusions}</p>
              </Col>
            </Row>
            <Row>
              <div className={"req-graph"}>
                <img style={{width: "70%", marginBottom: "3%"}} alt="" src={requisite_label}></img>
                <img src={`data:image/jpeg;base64,${this.state.graph}`} alt="" ></img>
              </div>
            </Row>
          </Row>
          <Row className="col-item course-keywords">
            <h3>Take this Course if You Like</h3>
            <p>{this.state.keywords}</p>
          </Row>
        </Container>
      </div>

		)
	}
}

export default CourseDescriptionPage
