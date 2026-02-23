"""Tests for Dockerfile Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate_dockerfile, list_languages, get_base_image, add_healthcheck, format_result_markdown, TEMPLATES

def test_python(): r = generate_dockerfile("python"); assert "python:3.11" in r.content
def test_node(): r = generate_dockerfile("node"); assert "node:20" in r.content
def test_go(): r = generate_dockerfile("go"); assert "golang" in r.content
def test_java(): r = generate_dockerfile("java"); assert "temurin" in r.content
def test_rust(): r = generate_dockerfile("rust"); assert "rust" in r.content
def test_static(): r = generate_dockerfile("static"); assert "nginx" in r.content
def test_unsupported(): r = generate_dockerfile("unknown"); assert "Unsupported" in r.content
def test_port(): r = generate_dockerfile("python", port=8080); assert "EXPOSE 8080" in r.content
def test_env(): r = generate_dockerfile("python", env_vars={"NODE_ENV": "production"}); assert "NODE_ENV" in r.content
def test_workdir(): r = generate_dockerfile("python"); assert "WORKDIR /app" in r.content
def test_copy_first(): r = generate_dockerfile("python"); assert "requirements.txt" in r.content
def test_list(): langs = list_languages(); assert "python" in langs and "node" in langs
def test_base_image(): assert "python" in get_base_image("python")
def test_base_missing(): assert get_base_image("unknown") == ""
def test_healthcheck(): hc = add_healthcheck("FROM python:3.11\n", port=3000); assert "HEALTHCHECK" in hc
def test_optimizations(): r = generate_dockerfile("python"); assert len(r.optimizations) >= 1
def test_format(): md = format_result_markdown(generate_dockerfile("python")); assert "Dockerfile" in md
def test_to_dict(): d = generate_dockerfile("python").to_dict(); assert "language" in d
def test_templates(): assert len(TEMPLATES) >= 5
