"""Tests for Text Case Converter."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import to_camel, to_pascal, to_snake, to_kebab, to_constant, to_title, to_sentence, detect_case, convert_all, format_result_markdown

def test_camel(): assert to_camel("hello world").converted == "helloWorld"
def test_pascal(): assert to_pascal("hello world").converted == "HelloWorld"
def test_snake(): assert to_snake("hello world").converted == "hello_world"
def test_kebab(): assert to_kebab("hello world").converted == "hello-world"
def test_constant(): assert to_constant("hello world").converted == "HELLO_WORLD"
def test_title(): assert to_title("hello world").converted == "Hello World"
def test_sentence(): assert to_sentence("hello world").converted == "Hello world"
def test_camel_from_snake(): assert to_camel("hello_world").converted == "helloWorld"
def test_pascal_from_kebab(): assert to_pascal("hello-world").converted == "HelloWorld"
def test_snake_from_camel(): assert to_snake("helloWorld").converted == "hello_world"
def test_detect_snake(): assert detect_case("hello_world") == "snake_case"
def test_detect_kebab(): assert detect_case("hello-world") == "kebab-case"
def test_detect_camel(): assert detect_case("helloWorld") == "camelCase"
def test_detect_pascal(): assert detect_case("HelloWorld") == "PascalCase"
def test_detect_constant(): assert detect_case("HELLO_WORLD") == "CONSTANT_CASE"
def test_convert_all(): d = convert_all("hello world"); assert "snake_case" in d
def test_format(): md = format_result_markdown(to_camel("hello world")); assert "Case Converter" in md
def test_to_dict(): d = to_camel("hello world").to_dict(); assert "converted" in d
