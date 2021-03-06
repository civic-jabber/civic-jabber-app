from copy import deepcopy
import datetime

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from civic_jabber_app.app import app
import civic_jabber_app.utils.database as database
import civic_jabber_app.regulations as regs


client = TestClient(app)


MOCK_REGULATIONS = [
    {
        "state": "va",
        "issue": "09",
        "volume": "37",
        "title": "20VAC5-204-40",
        "description": "Prudency determination filings",
        "status": "Final Regulation",
        "link": "http://register.dls.virginia.gov/details.aspx?id=9315",
        "start_date": datetime.datetime(2020, 12, 21, 0, 0),
        "end_date": None,
        "register_date": datetime.datetime(2020, 12, 21, 0, 0),
        "as_of_date": datetime.datetime(2020, 12, 23, 0, 24, 20, 151572),
    },
    {
        "state": "va",
        "issue": "09",
        "volume": "37",
        "title": "12VAC30-120",
        "description": "Waivered Services (amending 12VAC30-120-924)",
        "status": "Action Withdrawn",
        "link": "http://register.dls.virginia.gov/details.aspx?id=9323",
        "start_date": datetime.datetime(2020, 12, 21, 0, 0),
        "end_date": None,
        "register_date": datetime.datetime(2020, 12, 21, 0, 0),
        "as_of_date": datetime.datetime(2020, 12, 23, 0, 24, 18, 528879),
    },
]


def test_get_regulations(monkeypatch):
    monkeypatch.setattr(
        database, "execute_sql", lambda *args, **kwargs: MOCK_REGULATIONS
    )
    monkeypatch.setattr(regs, "count_regulations", lambda *args, **kwargs: 25)
    monkeypatch.setattr(database, "connect", lambda *args, **kwargs: "connection")
    response = client.get("/v1/regulations?state=va&page=1&limit=10")

    expected_results = deepcopy(MOCK_REGULATIONS)
    for result in expected_results:
        history = [deepcopy(result)]
        result["history"] = history

    assert response.status_code == 200
    assert response.json() == {
        "results": jsonable_encoder(expected_results),
        "count": 25,
        "page": 1,
        "limit": 10,
    }


def test_get_regulations_returns_422_with_bad_input(monkeypatch):
    monkeypatch.setattr(
        database, "execute_sql", lambda *args, **kwargs: MOCK_REGULATIONS
    )
    monkeypatch.setattr(database, "connect", lambda *args, **kwargs: "connection")
    response = client.get("/v1/regulations?state=va&order_by=lobsters")
    assert response.status_code == 422


def test_get_regulations_returns_400_without_state(monkeypatch):
    monkeypatch.setattr(
        database, "execute_sql", lambda *args, **kwargs: MOCK_REGULATIONS
    )
    monkeypatch.setattr(regs, "count_regulations", lambda *args, **kwargs: 25)
    monkeypatch.setattr(database, "connect", lambda *args, **kwargs: "connection")
    response = client.get("/v1/regulations")
    assert response.status_code == 400


def test_get_regulations_returns_400_with_value_error(monkeypatch):
    def mock_get_regulations(*args, **kwargs):
        raise ValueError("What a horrible error!")

    monkeypatch.setattr(regs, "get_regulations", mock_get_regulations)
    response = client.get("/v1/regulations?state=va")
    assert response.status_code == 400
