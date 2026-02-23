"""Tests for Docker Compose Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate_compose, list_templates, get_template, Service, SERVICE_TEMPLATES

def test_list_templates():
    templates = list_templates()
    assert "postgres" in templates and "redis" in templates

def test_template_count():
    assert len(list_templates()) >= 8

def test_get_template():
    t = get_template("postgres")
    assert t is not None and t.image == "postgres:16-alpine"

def test_get_unknown():
    assert get_template("unknown") is None

def test_generate_single():
    yml = generate_compose(["postgres"])
    assert "postgres" in yml
    assert "5432:5432" in yml

def test_generate_multi():
    yml = generate_compose(["postgres", "redis"])
    assert "postgres" in yml and "redis" in yml

def test_has_version():
    yml = generate_compose(["redis"])
    assert "version" in yml

def test_has_volumes():
    yml = generate_compose(["postgres"])
    assert "postgres_data" in yml

def test_has_env():
    yml = generate_compose(["postgres"])
    assert "POSTGRES_DB" in yml

def test_has_healthcheck():
    t = get_template("postgres")
    assert t.healthcheck is not None

def test_service_to_dict():
    t = get_template("redis")
    d = t.to_dict()
    assert "image" in d
    assert "ports" in d

def test_nginx_ports():
    yml = generate_compose(["nginx"])
    assert "80:80" in yml

def test_rabbitmq():
    yml = generate_compose(["rabbitmq"])
    assert "5672:5672" in yml

def test_skip_unknown():
    yml = generate_compose(["postgres", "nonexistent"])
    assert "postgres" in yml
    assert "nonexistent" not in yml

def test_restart_policy():
    t = get_template("redis")
    assert t.restart == "unless-stopped"
