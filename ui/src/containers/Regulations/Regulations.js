import axios from "axios";
import moment from "moment";
import React, { Component } from "react";

import RegsTable from "../../components/RegsTable/RegsTable";

class Regulations extends Component {
  constructor(props) {
    super(props);
    this.state = {
      rows: [],
    };
  }

  componentDidMount() {
    const url = "http://localhost:8000/api/v1/regulations";
    axios.get(url).then((res) => {
      let rows = [];
      for (let row of res.data) {
        if (row.register_date) {
          let register_date = moment(row.register_date, "YYYY-MM-DDTHH:mm:ss");
          row.register_date = register_date.format("YYYY-MM-DD");
        }

        if (row.start_date) {
          let start_date = moment(row.start_date, "YYYY-MM-DDTHH:mm:ss");
          row.start_date = start_date.format("YYYY-MM-DD");
        }

        if (row.end_date) {
          let end_date = moment(row.end_date, "YYYY-MM-DDTHH:mm:ss");
          row.end_date = end_date.format("YYYY-MM-DD");
        }

        rows.push(row);
      }
      this.setState({ rows });
    });
  }

  render() {
    return (
      <div>
        <RegsTable rows={this.state.rows} />
      </div>
    );
  }
}

export default Regulations;
