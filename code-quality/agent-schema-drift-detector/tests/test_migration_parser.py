def test_parse_migrations_basic(tmp_path):
    from lib.migration_parser import parse_migrations
    
    # Create simple migrations
    d = tmp_path / "migrations"
    d.mkdir()
    f1 = d / "001.sql"
    f1.write_text("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255));")
    f2 = d / "002.sql"
    f2.write_text("ALTER TABLE users ADD COLUMN age INTEGER;")
    
    schema = parse_migrations(d, "postgres")
    
    assert "users" in schema
    assert "id" in schema["users"]["columns"]
    assert "name" in schema["users"]["columns"]
    assert "email" in schema["users"]["columns"]
    assert "age" in schema["users"]["columns"]
    
    assert schema["users"]["columns"]["name"]["nullable"] is False
    assert schema["users"]["columns"]["email"]["nullable"] is True
    assert schema["users"]["columns"]["age"]["nullable"] is True

def test_parse_migrations_if_not_exists(tmp_path):
    from lib.migration_parser import parse_migrations
    f = tmp_path / "mig.sql"
    f.write_text('CREATE TABLE IF NOT EXISTS "public"."posts" ("id" serial, "title" text NOT NULL);')
    schema = parse_migrations(f, "postgres")

    assert "posts" in schema
    assert schema["posts"]["columns"]["title"]["nullable"] is False

def test_parse_migrations_add_column_not_null(tmp_path):
    from lib.migration_parser import parse_migrations
    f = tmp_path / "mig.sql"
    f.write_text('CREATE TABLE t (id int);\nALTER TABLE t ADD COLUMN flag boolean NOT NULL;')
    schema = parse_migrations(f, "postgres")
    assert schema["t"]["columns"]["flag"]["nullable"] is False

def test_parse_migrations_no_columns(tmp_path):
    from lib.migration_parser import parse_migrations
    f = tmp_path / "mig.sql"
    f.write_text('CREATE TABLE empty ();')
    schema = parse_migrations(f, "postgres")
    assert "empty" in schema
    assert not schema["empty"]["columns"]

def test_parse_migrations_missing_type(tmp_path):
    from lib.migration_parser import parse_migrations
    f = tmp_path / "mig.sql"
    f.write_text('CREATE TABLE missing (id); ALTER TABLE missing ADD missing_type;')
    schema = parse_migrations(f, "postgres")
    assert schema["missing"]["columns"]["id"]["type"] == "UNKNOWN"
    assert schema["missing"]["columns"]["missing_type"]["type"] == "UNKNOWN"
