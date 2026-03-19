import pytest
from click.testing import CliRunner
from main import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_no_drift(runner, tmp_path, mocker):
    mocker.patch("main.parse_migrations", return_value={"users": {"columns": {"id": {"nullable": False}}}})
    mocker.patch("main.parse_orm_models", return_value={"users": {"columns": {"id": {"nullable": False}}}})
    
    mig = tmp_path / "mig.sql"
    mig.touch()
    orm = tmp_path / "schema.prisma"
    orm.touch()
    
    cfg = tmp_path / "config.yaml"
    cfg.write_text(f"migrations: ['{mig}']\norm_models: ['{orm}']\n")
    
    result = runner.invoke(cli, ["--config", str(cfg)])
    assert result.exit_code == 0
    assert "No schema drift detected" in result.output

def test_cli_with_drift(runner, tmp_path, mocker):
    mocker.patch("main.parse_migrations", return_value={"users": {"columns": {"id": {"nullable": False}}}})
    mocker.patch("main.parse_orm_models", return_value={})
    
    mig = tmp_path / "mig.sql"
    mig.touch()
    orm = tmp_path / "schema.prisma"
    orm.touch()
    
    cfg = tmp_path / "config.yaml"
    cfg.write_text(f"migrations: ['{mig}']\norm_models: ['{orm}']\n")
    
    result = runner.invoke(cli, ["--config", str(cfg)])
    assert result.exit_code == 1
    assert "Drift detected!" in result.output

def test_cli_json_format(runner, tmp_path, mocker):
    mocker.patch("main.parse_migrations", return_value={"users": {"columns": {"id": {"nullable": False}}}})
    mocker.patch("main.parse_orm_models", return_value={})
    
    mig = tmp_path / "mig.sql"
    mig.touch()
    orm = tmp_path / "schema.prisma"
    orm.touch()
    
    result = runner.invoke(cli, ["--format", "json", "-m", str(mig), "-o", str(orm)])
    assert result.exit_code == 1
    assert "missing_table" in result.output

def test_cli_markdown_format(runner, tmp_path, mocker):
    mocker.patch("main.parse_migrations", return_value={"users": {"columns": {"id": {"nullable": False}}}})
    mocker.patch("main.parse_orm_models", return_value={})
    
    mig = tmp_path / "mig.sql"
    mig.touch()
    orm = tmp_path / "schema.prisma"
    orm.touch()
    
    result = runner.invoke(cli, ["--format", "markdown", "-m", str(mig), "-o", str(orm)])
    assert result.exit_code == 1
    assert "## Schema Drift Report" in result.output

def test_load_config_default(runner, tmp_path):
    # Ensure graceful handling when config file does not exist
    result = runner.invoke(cli, ["--config", "does_not_exist.yaml"])
    assert result.exit_code == 0 # assuming default config has no drift
