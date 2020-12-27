import civic_jabber_app.regulations as regs
import civic_jabber_app.utils.database as database


def test_count_regulations(monkeypatch):
    monkeypatch.setattr(
        database, "execute_sql", lambda *args, **kwargs: [{"result_size": 25}]
    )
    assert regs.count_regulations("fake_connection") == 25
