import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

import civic_jabber_app.utils.database as database


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
        ORDER BY {order_by} {order}, id {order}
        OFFSET {offset}
        LIMIT {limit}
    """
    results = database.execute_sql(sql, connection, select=True)
    return jsonable_encoder([dict(result) for result in results])
