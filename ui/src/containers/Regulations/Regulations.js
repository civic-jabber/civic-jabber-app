import axios from "axios";
import moment from "moment";
import React, { Component } from "react";

import RegsTable from "../../components/RegsTable/RegsTable";

function formatDate(date) {
  // Formats the date so that it displays appropriately in the table
  //
  // Parameters
  // ----------
  // date : string
  //    The date string to formate
  //
  //  Returns
  //  -------
  //  formattedDate : Date
  //    A moment formatted date
  if (date) {
    let formattedDate = moment(date, "YYYY-MM-DDTHH:mm:ss");
    return formattedDate.format("YYYY-MM-DD");
  } else {
    return date;
  }
}

class Regulations extends Component {
  constructor(props) {
    super(props);
    this.state = {
      rows: [],
      page: 1,
      count: 0,
      limit: 10,
      stateCode: null, // We can default this to what gets pulled from the URL
    };
  }

  componentDidMount() {
    this.fetchResults("va", 1, this.state.limit);
  }

  fetchResults(stateCode, page, limit) {
    // Updates the table with the specified results set
    //
    // Parameters
    // ----------
    // stateCode : string
    //    The two letter code for the state
    // page : integer
    //    The page of results to return. Indexed to 1.
    const baseURL = "http://localhost:8000/v1";
    const url = `${baseURL}/regulations?state=${stateCode}&page=${page}&limit=${limit}`;
    axios.get(url).then((res) => {
      let rows = [];
      for (let row of res.data.results) {
        row.register_date = formatDate(row.register_date);
        row.start_date = formatDate(row.start_date);
        row.end_date = formatDate(row.end_date);
        rows.push(row);
      }
      let page = res.data.page;
      let count = res.data.count;
      console.log(rows);
      this.setState({ rows, page, count, limit, stateCode });
    });
  }

  render() {
    return (
      <div>
        <h2>Virginia Regulations</h2>
        <hr />
        <RegsTable
          rows={this.state.rows}
          page={this.state.page}
          count={this.state.count}
          limit={this.state.limit}
          fetch={(stateCode, page, limit) =>
            this.fetchResults(stateCode, page, limit)
          }
          stateCode={this.state.stateCode}
        />
      </div>
    );
  }
}

export default Regulations;
