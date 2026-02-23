"""Tests for CRUD API Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import Model, ModelField, generate_express_routes, generate_fastapi_routes, parse_model_definition, list_endpoints

USER_MODEL = Model(name="User", fields=[ModelField(name="name", type="string", required=True), ModelField(name="email", type="string", required=True), ModelField(name="age", type="number", required=False)])

def test_express_has_get():
    code = generate_express_routes(USER_MODEL)
    assert 'router.get("/users"' in code

def test_express_has_post():
    code = generate_express_routes(USER_MODEL)
    assert 'router.post("/users"' in code

def test_express_has_put():
    code = generate_express_routes(USER_MODEL)
    assert 'router.put("/users/:id"' in code

def test_express_has_delete():
    code = generate_express_routes(USER_MODEL)
    assert 'router.delete("/users/:id"' in code

def test_express_validation():
    code = generate_express_routes(USER_MODEL)
    assert '"name"' in code and '"email"' in code

def test_express_timestamps():
    code = generate_express_routes(USER_MODEL)
    assert "createdAt" in code

def test_fastapi_has_routes():
    code = generate_fastapi_routes(USER_MODEL)
    assert '@router.get("/users")' in code
    assert '@router.post("/users"' in code

def test_fastapi_model():
    code = generate_fastapi_routes(USER_MODEL)
    assert "class UserCreate" in code
    assert "name: str" in code

def test_fastapi_optional():
    code = generate_fastapi_routes(USER_MODEL)
    assert "Optional" in code

def test_parse_simple():
    m = parse_model_definition("Product: title:string, price:number")
    assert m.name == "Product"
    assert len(m.fields) == 2

def test_parse_name_only():
    m = parse_model_definition("Item")
    assert m.name == "Item"

def test_list_endpoints():
    eps = list_endpoints(USER_MODEL)
    assert len(eps) == 5
    methods = [e["method"] for e in eps]
    assert "GET" in methods and "POST" in methods and "DELETE" in methods

def test_model_to_dict():
    d = USER_MODEL.to_dict()
    assert d["name"] == "User"
    assert len(d["fields"]) == 3

def test_no_timestamps():
    m = Model(name="Log", fields=[], timestamps=False)
    code = generate_express_routes(m)
    assert "createdAt" not in code

def test_express_is_valid_js():
    code = generate_express_routes(USER_MODEL)
    assert "module.exports" in code
    assert "express" in code
