import pytest
from agent.data_generator import DataGenerator

def test_generate_formats():
    gen = DataGenerator()

    assert isinstance(gen.generate_from_schema({'type': 'string', 'format': 'uuid'}), str)
    assert isinstance(gen.generate_from_schema({'type': 'string', 'format': 'date'}), str)
    assert isinstance(gen.generate_from_schema({'type': 'string', 'format': 'uri'}), str)
    assert isinstance(gen.generate_from_schema({'type': 'string', 'format': 'url'}), str)
    assert isinstance(gen.generate_from_schema({'type': 'string', 'format': 'date-time'}), str)

def test_generate_enum():
    gen = DataGenerator()
    schema = {'type': 'string', 'enum': ['A', 'B']}
    assert gen.generate_from_schema(schema) in ['A', 'B']

def test_generate_one_of():
    gen = DataGenerator()
    schema = {'oneOf': [{'type': 'string'}, {'type': 'integer'}]}
    # Implementation picks first
    assert isinstance(gen.generate_from_schema(schema), str)

def test_generate_any_of():
    gen = DataGenerator()
    schema = {'anyOf': [{'type': 'integer'}, {'type': 'string'}]}
    # Implementation picks first
    assert isinstance(gen.generate_from_schema(schema), int)

def test_generate_number():
    gen = DataGenerator()
    schema = {'type': 'number', 'minimum': 1.0, 'maximum': 2.0}
    val = gen.generate_from_schema(schema)
    assert isinstance(val, float)
    assert 1.0 <= val <= 2.0

def test_generate_heuristics_extended():
    gen = DataGenerator()
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='phone'), str)
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='address'), str)
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='city'), str)
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='country'), str)
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='job'), str)
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='color'), str)
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='description'), str)
    assert isinstance(gen.generate_from_schema({'type': 'string'}, field_name='username'), str)

def test_fallback():
    gen = DataGenerator()
    assert gen.generate_from_schema(None) == {}
    assert gen.generate_from_schema({}) == {} # Empty schema -> Empty dict or None? implementation returns {}
    # Test implicit object
    assert isinstance(gen.generate_from_schema({'properties': {'a': {'type': 'string'}}}), dict)
