import pytest
from agent.data_generator import DataGenerator

def test_generate_simple_types():
    gen = DataGenerator()

    assert isinstance(gen.generate_from_schema({'type': 'string'}), str)
    assert isinstance(gen.generate_from_schema({'type': 'integer'}), int)
    assert isinstance(gen.generate_from_schema({'type': 'boolean'}), bool)

def test_generate_object():
    gen = DataGenerator()
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'age': {'type': 'integer', 'minimum': 18, 'maximum': 99}
        }
    }
    data = gen.generate_from_schema(schema)
    assert isinstance(data, dict)
    assert 'name' in data
    assert 'age' in data
    assert 18 <= data['age'] <= 99

def test_generate_array():
    gen = DataGenerator()
    schema = {
        'type': 'array',
        'items': {'type': 'string'},
        'minItems': 2,
        'maxItems': 5
    }
    data = gen.generate_from_schema(schema)
    assert isinstance(data, list)
    assert 2 <= len(data) <= 5
    assert all(isinstance(x, str) for x in data)

def test_generate_heuristics():
    gen = DataGenerator()
    # Test name heuristic
    schema = {'type': 'string'}
    name = gen.generate_from_schema(schema, field_name='full_name')
    # Can't easily verify it's a name, but we can verify it's a string
    assert isinstance(name, str)

    # Test email format
    email_schema = {'type': 'string', 'format': 'email'}
    email = gen.generate_from_schema(email_schema)
    assert '@' in email
