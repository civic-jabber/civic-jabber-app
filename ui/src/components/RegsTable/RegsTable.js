import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TablePagination from "@material-ui/core/TablePagination";
import TableRow from "@material-ui/core/TableRow";

const columns = [
  { id: "title", label: "Title", minWidth: 100 },
  { id: "status", label: "Status", minWidth: 100 },
  {
    id: "description",
    label: "Description",
    minWidth: 170,
    align: "left",
  },
  {
    id: "volume",
    label: "Volume",
    minWidth: 50,
    align: "left",
  },
  {
    id: "issue",
    label: "Issue",
    minWidth: 50,
    align: "right",
  },
  {
    id: "start_date",
    label: "Start Date",
    minWidth: 80,
    align: "left",
  },
  {
    id: "register_date",
    label: "Register Date",
    minWidth: 80,
    align: "left",
  },
];

const useStyles = makeStyles({
  root: {
    width: "100%",
    margin: "auto",
  },
  container: {
    maxHeight: 800,
  },
});

export default function RegsTable(props) {
  const classes = useStyles();
  let setPage = (page, limit) => {
    props.fetch(props.stateCode, page, limit);
  };
  let page = props.page - 1;

  const handleChangePage = (event, newPage) => {
    setPage(newPage + 1, props.limit);
  };

  const handleChangeRowsPerPage = (event) => {
    const rowsPerPage = +event.target.value;
    console.log(rowsPerPage);
    setPage(1, rowsPerPage);
  };

  return (
    <Paper className={classes.root}>
      <TableContainer className={classes.container}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{ minWidth: column.minWidth }}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {props.rows.map((row) => {
              return (
                <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>
                  {columns.map((column) => {
                    const value = row[column.id];
                    return (
                      <TableCell key={column.id} align={column.align}>
                        {column.format && typeof value === "number"
                          ? column.format(value)
                          : value}
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={props.count}
        rowsPerPage={props.limit}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
      />
    </Paper>
  );
}
