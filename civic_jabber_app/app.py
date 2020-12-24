from typing import Optional

from fastapi import FastAPI, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import civic_jabber_app.utils.database as database

app = FastAPI()


def get_regulations(limit=25, offset=0, order_by="register_date", order="DESC"):
    if order.upper() not in ["ASC", "DESC"]:
        raise ValueError("Valid options for order as ASC and DESC")

    order_cols = [
        "register_date",
        "issue",
        "volume",
        "start_date",
        "end_date",
        "status",
    ]
    if order_by.lower() not in order_cols:
        raise ValueError(f"{order_by} is not a valid column for ordering.")

    connection = database.connect()
    sql = f"""
        SELECT DISTINCT
            id,
            state,
            issue,
            volume,
            title,
            description,
            status,
            link,
            CASE
                WHEN date IS NOT NULL THEN date
                WHEN register_date IS NOT NULL THEN register_date
                ELSE start_date
            END as start_date,
            end_date,
            register_date
        FROM civic_jabber.titles
        ORDER BY {order_by}, id {order}
        OFFSET {offset}
        LIMIT {limit}
    """
    results = database.execute_sql(sql, connection, select=True)
    return jsonable_encoder([dict(result) for result in results])


@app.get("/api/v1/regulations")
async def regulations(
    limit: Optional[int] = Query(25),
    page: Optional[int] = Query(1),
    order_by: Optional[str] = Query("register_date"),
    order: Optional[str] = Query("DESC"),
):
    """Queries the Postgres table for regulations

    Parameters
    ----------
    limit : int
        The number of results to return per page
    page : int
        The page number, starting at 1
    order_by : str
        The column to order the results by
    order: str
        The order in which to return the results. Valid values are asc and desc

    Returns
    -------
    regulations : list
        A list of dictionary objects representing the regulations
    """
    offset = (page - 1) * limit
    try:
        msg = get_regulations(
            limit=limit, offset=offset, order_by=order_by, order=order
        )
        status_code = status.HTTP_200_OK
    except ValueError:
        msg = {"message": "Bad Request"}
        status_code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(status_code=status_code, content=msg)
