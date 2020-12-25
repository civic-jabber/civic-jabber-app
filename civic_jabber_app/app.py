import datetime
from typing import List, Optional

from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import civic_jabber_app.utils.database as database

app = FastAPI()

origins = [
    "http://localhost*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegulationResponse(BaseModel):
    id: str
    state: str
    issue: str
    title: str
    description: str
    status: str
    link: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    register_date: datetime.datetime


def get_regulations(limit=25, offset=0, order_by="register_date", order="DESC"):
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


ORDER_BY_OPTIONS = "^(issue|volume|title|description|(start|end|register)_date)$"
ORDER_OPTIONS = "^(?i)(asc|desc)$"


@app.get("/api/v1/regulations", response_model=List[RegulationResponse])
async def regulations(
    limit: Optional[int] = Query(25),
    page: Optional[int] = Query(1),
    order_by: Optional[str] = Query("register_date", regex=ORDER_BY_OPTIONS),
    order: Optional[str] = Query("DESC", regex=ORDER_OPTIONS),
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
