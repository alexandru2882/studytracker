from studytracker.logic import add_session, list_sessions, total_minutes


def test_add_list_total(tmp_path, monkeypatch):
    # Redirect data to a temp folder so tests don't touch your real files
    monkeypatch.setenv("STUDYTRACKER_HOME", str(tmp_path))

    assert list_sessions() == []
    add_session("Python", 30, "2025-01-01")
    add_session("Math", 45, "2025-01-02")
    add_session("Python", 25, "2025-01-03")

    items = list_sessions()
    assert len(items) == 3
    assert total_minutes() == 100
    assert total_minutes("python") == 55
