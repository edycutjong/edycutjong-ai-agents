from main import run, extract_functions, generate_test_cases, generate_test_file, format_preview


def test_run():
    assert "Test Case Generator" in run("test")


SAMPLE = '''
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str):
    print(f"Hello {name}")
'''


def test_extract_functions():
    funcs = extract_functions(SAMPLE)
    assert len(funcs) == 2
    assert funcs[0]["name"] == "add"
    assert len(funcs[0]["params"]) == 2


def test_extract_no_functions():
    assert extract_functions("x = 1") == []


def test_extract_syntax_error():
    assert extract_functions("def broken(") == []


def test_generate_test_cases():
    func = {"name": "add", "params": [{"name": "a", "type": "int"}, {"name": "b", "type": "int"}],
            "has_return": True, "is_async": False, "lineno": 1}
    cases = generate_test_cases(func)
    assert len(cases) >= 2
    assert cases[0]["kind"] == "happy"


def test_generate_test_file():
    funcs = extract_functions(SAMPLE)
    code = generate_test_file(funcs, "sample")
    assert "import pytest" in code
    assert "test_add_happy_path" in code


def test_format_preview():
    funcs = extract_functions(SAMPLE)
    preview = format_preview(funcs)
    assert "add" in preview
    assert "greet" in preview
