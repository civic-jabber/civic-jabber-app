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


def _base_query():
    return """
        SELECT
            id,
            titles.state,
            issue,
            volume,
            titles.title,
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
    """


def get_regulations(state, limit=25, page=1, order_by="register_date", order="DESC"):
    connection = database.connect()
    offset = (page - 1) * limit
    sql = f"""
        {_base_query()}
        INNER JOIN (
            {_group_by_query()}
        ) as latest
        ON latest.max_id = titles.id
        ORDER BY {order_by} {order}, id {order}
        OFFSET {offset}
        LIMIT {limit}
    """
    results = database.execute_sql(sql, connection, select=True)
    titles = [result["title"] for result in results]
    histories = get_status_histories(titles, state, connection=connection)

    results = jsonable_encoder([dict(result) for result in results])
    final_results = list()
    for result in results:
        final_result = jsonable_encoder(dict(result))
        final_result["history"] = jsonable_encoder(histories[result["title"]])
        final_results.append(final_result)

    return {
        "results": final_results,
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


def get_status_histories(titles, state, connection=None):
    """Returns the status histories for each of the specified titles

    Parameters
    ----------
    titles : list
        A list of titles
    state : str
        The state the titles are associated with

    Returns
    -------
    histories : dict
        A dictionary where the keys are titles and the entries are lists that show the
        status history for the title
    """
    connection = database.connect() if not connection else connection
    where_clause = ", ".join([f"'{title}'" for title in titles])
    sql = f"""
       {_base_query()}
       WHERE title in ({where_clause})
       ORDER BY title, register_date DESC
    """
    results = database.execute_sql(sql, connection, select=True)
    histories = dict()
    for result in results:
        title_history = histories.get(result["title"], [])
        title_history.append(dict(result))
        histories[result["title"]] = title_history
    return histories
