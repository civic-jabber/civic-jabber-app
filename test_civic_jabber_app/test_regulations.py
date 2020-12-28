import datetime

import civic_jabber_app.regulations as regs
import civic_jabber_app.utils.database as database


def test_count_regulations(monkeypatch):
    monkeypatch.setattr(
        database, "execute_sql", lambda *args, **kwargs: [{"result_size": 25}]
    )
    assert regs.count_regulations("fake_connection") == 25


MOCK_HISTORY = [
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
    {
        "state": "va",
        "issue": "09",
        "volume": "37",
        "title": "20VAC5-204-40",
        "description": "Prudency determination filings",
        "status": "Final Regulation",
        "link": "http://register.dls.virginia.gov/details.aspx?id=9315",
        "start_date": datetime.datetime(2019, 12, 21, 0, 0),
        "end_date": None,
        "register_date": datetime.datetime(2019, 12, 21, 0, 0),
        "as_of_date": datetime.datetime(2019, 12, 23, 0, 24, 20, 151572),
    },
]


def test_get_status_histories(monkeypatch):
    monkeypatch.setattr(database, "execute_sql", lambda *args, **kwargs: MOCK_HISTORY)
    assert regs.get_status_histories(
        ["20VAC5-204-40", "12VAC30-120"], "va", "fake_connection"
    ) == {
        "20VAC5-204-40": [MOCK_HISTORY[0], MOCK_HISTORY[2]],
        "12VAC30-120": [MOCK_HISTORY[1]],
    }
