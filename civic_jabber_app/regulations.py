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


def _group_by_query():
    return """
        SELECT
            state,
            title,
            MAX(register_date) AS max_register_date,
            MAX(id) as max_id
        FROM civic_jabber.titles
        GROUP BY state, title
    """


def get_regulations(state, limit=25, page=1, order_by="register_date", order="DESC"):
    connection = database.connect()
    offset = (page - 1) * limit
    sql = f"""
        SELECT DISTINCT
            id,
            latest.state,
            issue,
            volume,
            latest.title,
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
        FROM civic_jabber.titles as titles
        INNER JOIN (
            {_group_by_query()}
        ) as latest
        ON latest.max_id = titles.id
        ORDER BY {order_by} {order}, id {order}
        OFFSET {offset}
        LIMIT {limit}
    """
    results = database.execute_sql(sql, connection, select=True)
    return {
        "results": jsonable_encoder([dict(result) for result in results]),
        "count": count_regulations(connection=connection),
        "page": page,
        "limit": limit,
    }


def count_regulations(connection=None):
    connection = database.connect() if not connection else connection
    sql = f"""
        SELECT COUNT(*) as result_size
        FROM (
            {_group_by_query()}
        ) as latest
    """
    results = database.execute_sql(sql, connection, select=True)
    return results[0]["result_size"]
