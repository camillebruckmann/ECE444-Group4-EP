import React, { Component } from "react";
import Multiselect from 'multiselect-react-dropdown';
import axios from 'axios'
import Result from './Results'
import './css/Result.css'
import Label from './Label'
import "./css/styles.css";
import API from '../api';


class SearchResultDisplay extends Component{

  constructor() {
    super();
    this.state = {
      input: "",
      results: []
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleSubmit2 = this.handleSubmit2.bind(this);
  }

  handleChange(event) {
    this.setState({input: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    this.getData(this.state.input)
  }

  handleSubmit2(event) {
    event.preventDefault();
    this.getData("hi")
  }

  getData = (input) => {
    API.get(`/searchc?input=${input}`)
      .then(res => {
        if (res.status === 200) {
          this.setState({results: []})
          console.log(res.data.length)
          if (res.data.length > 0) {
            let len = res.data.length
            let result_temp = []
            result_temp.push(<Label></Label>)
            for (let i = 0; i < len; i++) {
                result_temp.push(<Result key={res.data[i]._id} course_code={res.data[i].code} course_name={res.data[i].name}></Result>)
            }
            this.setState({results: result_temp})
          } 
          else
            if (res.data.length === 0) {
              alert("Course not found")
            }
            else {
              let result_temp = []
              result_temp.push(<Label></Label>)
              result_temp.push(<Result key={res.data.course._id} course_code={res.data.course.code} course_name={res.data.course.name}></Result>)
              this.setState({results: result_temp})
            }
        } else if (res.status === 400) {
          alert("System Error. Please refresh")
        }
    })
  }

  // search_render = (input) => {

  //   <div className="SearchQuery">
  //       <div style={{ marginTop: "10%" }}>
  //           <h1> Education Pathways Search</h1>
  //           <br></br>
  //           <form onSubmit={this.handleSubmit} className={"search"}>
  //               <input placeholder={"Search for course code, course name, keyword ..."} className={"text-input"} type="text" value={this.state.input} onChange={this.handleChange} />
  //               <input type="submit" value="Submit" className={"submit-button"}/>
  //           </form>
  //       </div>

  //       <div className={"search-result-display"} >
  //           {this.state.results}
  //       </div>

       
  //     </div>





  // }

  render(){
    return (
      <div className="SearchQuery">
        <div style={{ marginTop: "10%" }}>
            <h1> Education pathways</h1>
            <br></br>
            {/* <div className = "body_text">
      Welcome to CARTE's in-development tool for course selection at UofT. Education Pathways allows for more intelligent course searching, by matching not just the terms you search, but ones relevant to them. The more terms you search for, the more relevant your results will be! Even try searching across disciplines for the courses that best cover each.

Whatever year you are looking for, Education Pathways will also suggest courses in earlier years that will best help you to prepare. To get the most out of this, try searching for courses in a later year and see what is suggested for your current one.

We are looking for feedback to improve Education Pathways and make it more useful for students. If you have ideas or suggestions, please <a href = "mailto:alex.olson@utoronto.ca">  email us! </a>


      </div> */}
            <form className={"search"}>
            
                <input placeholder={"Search for course code"} className={"text-input"} type="text" value={this.state.input} onChange={this.handleChange} />
                <input type="submit" value="Search" onClick={this.handleSubmit} className={"submit-button"}/>
                <Multiselect className={"filters"}
                  displayValue="key"
                  groupBy="cat"
                  onKeyPressFn={(event)=>{console.log(event)}}
                  onRemove={(event)=>{console.log(event)}}
                  onSearch={(event)=>{console.log(event)}}
                  onSelect={(event)=>{console.log(event)}}
                  placeholder="Click to add filters"
                  hidePlaceholder = 'true'
                  style={{
                    chips: {
                      background: '#05285e',
                      color: 'white'
                    },
                    multiselectContainer: {
                      'margin': 'auto'
                    },
                    searchBox: {
                      border: 'none',
                      width: '49%',
                      height: '3em',
                      'align-items': 'center',
                      'border': '2px solid #a6c9ff',
                      'border-radius': '15px',
                      'background-color': '#a6c9ff',
                      'margin': '10px auto',
                      'padding-left': '2%'
                    }
                  }}
                  options={[
                    {
                      cat: 'Session',
                      key: 'Fall'
                    },
                    {
                      cat: 'Session',
                      key: 'Winter'
                    },
                    {
                      cat: 'Session',
                      key: 'Summer'
                    },
                    {
                      cat: 'Campus',
                      key: 'St. George'
                    },
                    {
                      cat: 'Campus',
                      key: 'Mississauga'
                    },
                    {
                      cat: 'Campus',
                      key: 'Scarborough'
                    },
                    {
                      cat: 'Group 2',
                      key: 'Option 7'
                    }
                  ]}
                  
                  /> 
            </form>
            
            
        </div>

        <div className={"search-result-display"} >
            {this.state.results}
        </div>

       
      </div>
    );
  }


  
}

export default SearchResultDisplay;
