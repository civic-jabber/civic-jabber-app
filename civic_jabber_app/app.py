from typing import List, Optional

from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import civic_jabber_app.regulations as regs

app = FastAPI()

origins = [
    "http://localhost*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ORDER_BY_OPTIONS = "^(issue|volume|title|description|(start|end|register)_date)$"
ORDER_OPTIONS = "^(?i)(asc|desc)$"


@app.get("/api/v1/regulations", response_model=List[regs.RegulationResponse])
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
        msg = regs.get_regulations(
            limit=limit, offset=offset, order_by=order_by, order=order
        )
        status_code = status.HTTP_200_OK
    except ValueError:
        msg = {"message": "Bad Request"}
        status_code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(status_code=status_code, content=msg)
