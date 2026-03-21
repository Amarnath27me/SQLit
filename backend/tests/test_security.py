from app.core.security import validate_query


def test_valid_select():
    ok, err = validate_query("SELECT * FROM users")
    assert ok is True
    assert err is None


def test_block_drop():
    ok, err = validate_query("DROP TABLE users")
    assert ok is False
    assert "SELECT" in err


def test_block_delete():
    ok, err = validate_query("DELETE FROM users")
    assert ok is False


def test_block_multi_statement():
    ok, err = validate_query("SELECT 1; DROP TABLE users")
    assert ok is False


def test_block_insert_in_select():
    ok, err = validate_query("SELECT * FROM users; INSERT INTO users VALUES (1)")
    assert ok is False


def test_empty_query():
    ok, err = validate_query("")
    assert ok is False
