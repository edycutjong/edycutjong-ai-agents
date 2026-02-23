"""Tests for GitHub Actions Writer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.writer import WorkflowConfig, generate_workflow, workflow_to_yaml, list_templates, format_templates_markdown, WORKFLOW_TEMPLATES

def test_list_templates():
    t = list_templates()
    assert len(t) >= 6
    assert "node-ci" in t

def test_generate_node():
    w = generate_workflow(WorkflowConfig(template="node-ci"))
    assert w["name"] == "Node.js CI"
    assert "build" in w["jobs"]

def test_generate_python():
    w = generate_workflow(WorkflowConfig(template="python-ci"))
    assert "test" in w["jobs"]

def test_generate_docker():
    w = generate_workflow(WorkflowConfig(template="docker-build"))
    assert w["name"] == "Docker Build"

def test_generate_vercel():
    w = generate_workflow(WorkflowConfig(template="deploy-vercel"))
    assert "deploy" in w["jobs"]

def test_generate_lint():
    w = generate_workflow(WorkflowConfig(template="lint"))
    assert "lint" in w["jobs"]

def test_generate_release():
    w = generate_workflow(WorkflowConfig(template="release"))
    assert "tags" in str(w["on"])

def test_custom_name():
    w = generate_workflow(WorkflowConfig(template="node-ci", name="My CI"))
    assert w["name"] == "My CI"

def test_unknown_template():
    with pytest.raises(ValueError):
        generate_workflow(WorkflowConfig(template="nonexistent"))

def test_yaml_output():
    w = generate_workflow(WorkflowConfig(template="node-ci"))
    yaml = workflow_to_yaml(w)
    assert "name:" in yaml
    assert "checkout" in yaml

def test_yaml_has_on():
    w = generate_workflow(WorkflowConfig(template="python-ci"))
    yaml = workflow_to_yaml(w)
    assert "on:" in yaml

def test_yaml_has_steps():
    w = generate_workflow(WorkflowConfig(template="node-ci"))
    yaml = workflow_to_yaml(w)
    assert "steps:" in yaml

def test_all_templates_valid():
    for name in WORKFLOW_TEMPLATES:
        w = generate_workflow(WorkflowConfig(template=name))
        assert "name" in w
        assert "on" in w
        assert "jobs" in w

def test_format_templates_markdown():
    md = format_templates_markdown()
    assert "GitHub Actions Templates" in md
    assert "node-ci" in md

def test_checkout_in_all():
    for name in WORKFLOW_TEMPLATES:
        w = generate_workflow(WorkflowConfig(template=name))
        steps = list(w["jobs"].values())[0]["steps"]
        assert any("checkout" in str(s) for s in steps)
