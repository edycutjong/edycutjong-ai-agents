"""Tests for GraphQL Schema Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import parse_schema, get_schema_stats, find_unused_types, find_complexity_issues, format_analysis_markdown

SAMPLE_SCHEMA = """
scalar DateTime

enum Role {
  ADMIN
  USER
  MODERATOR
}

interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
  email: String!
  role: Role!
  posts: [Post!]!
  createdAt: DateTime
}

type Post implements Node {
  id: ID!
  title: String!
  body: String
  author: User!
  tags: [String!]
}

input CreateUserInput {
  name: String!
  email: String!
  role: Role
}

union SearchResult = User | Post

type Query {
  user(id: ID!): User
  users(limit: Int): [User!]!
  post(id: ID!): Post
  search(query: String!): [SearchResult!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Orphan {
  data: String
}
"""

def test_parse_types():
    types = parse_schema(SAMPLE_SCHEMA)
    names = [t.name for t in types]
    assert "User" in names
    assert "Post" in names

def test_parse_enum():
    types = parse_schema(SAMPLE_SCHEMA)
    role = next(t for t in types if t.name == "Role")
    assert role.kind == "enum"
    assert "ADMIN" in role.values

def test_parse_scalar():
    types = parse_schema(SAMPLE_SCHEMA)
    dt = next(t for t in types if t.name == "DateTime")
    assert dt.kind == "scalar"

def test_parse_union():
    types = parse_schema(SAMPLE_SCHEMA)
    sr = next(t for t in types if t.name == "SearchResult")
    assert sr.kind == "union"
    assert "User" in sr.values

def test_parse_interface():
    types = parse_schema(SAMPLE_SCHEMA)
    node = next(t for t in types if t.name == "Node")
    assert node.kind == "interface"

def test_parse_implements():
    types = parse_schema(SAMPLE_SCHEMA)
    user = next(t for t in types if t.name == "User")
    assert "Node" in user.implements

def test_parse_fields():
    types = parse_schema(SAMPLE_SCHEMA)
    user = next(t for t in types if t.name == "User")
    field_names = [f.name for f in user.fields]
    assert "name" in field_names
    assert "email" in field_names

def test_required_fields():
    types = parse_schema(SAMPLE_SCHEMA)
    user = next(t for t in types if t.name == "User")
    name_field = next(f for f in user.fields if f.name == "name")
    assert name_field.is_required

def test_list_fields():
    types = parse_schema(SAMPLE_SCHEMA)
    user = next(t for t in types if t.name == "User")
    posts_field = next(f for f in user.fields if f.name == "posts")
    assert posts_field.is_list

def test_input_type():
    types = parse_schema(SAMPLE_SCHEMA)
    inp = next(t for t in types if t.name == "CreateUserInput")
    assert inp.kind == "input"

def test_stats():
    types = parse_schema(SAMPLE_SCHEMA)
    stats = get_schema_stats(types)
    assert stats.queries == 4
    assert stats.mutations == 2
    assert stats.enums == 1
    assert stats.scalars == 1

def test_unused_types():
    types = parse_schema(SAMPLE_SCHEMA)
    unused = find_unused_types(types)
    assert "Orphan" in unused

def test_no_issues_small_schema():
    types = parse_schema(SAMPLE_SCHEMA)
    issues = find_complexity_issues(types)
    assert not any("User" in i for i in issues)

def test_format_markdown():
    types = parse_schema(SAMPLE_SCHEMA)
    stats = get_schema_stats(types)
    md = format_analysis_markdown(types, stats)
    assert "Schema Analysis" in md
    assert "User" in md

def test_to_dict():
    types = parse_schema(SAMPLE_SCHEMA)
    d = types[0].to_dict()
    assert "name" in d
    assert "kind" in d

def test_empty_schema():
    types = parse_schema("")
    assert len(types) == 0

def test_field_args():
    types = parse_schema(SAMPLE_SCHEMA)
    query = next(t for t in types if t.name == "Query")
    user_field = next(f for f in query.fields if f.name == "user")
    assert "id" in user_field.args


# --- Cover remaining lines ---
def test_to_dict_with_fields_and_implements():
    """Cover lines 32, 34."""
    from agent.analyzer import TypeInfo, FieldInfo
    t = TypeInfo(name="Dog", kind="type", fields=[FieldInfo(name="name", field_type="String")], implements=["Animal"])
    d = t.to_dict()
    assert "fields" in d
    assert "implements" in d

def test_subscription_stats():
    """Cover line 124."""
    sdl = """type Subscription { messageAdded: String }"""
    types = parse_schema(sdl)
    stats = get_schema_stats(types)
    assert stats.subscriptions == 1

def test_complexity_many_fields():
    """Cover line 159 — type with >20 fields."""
    from agent.analyzer import TypeInfo, FieldInfo, find_complexity_issues
    fields = [FieldInfo(name=f"f{i}", field_type="String") for i in range(25)]
    t = TypeInfo(name="Big", kind="type", fields=fields)
    issues = find_complexity_issues([t])
    assert any("25 fields" in i for i in issues)

def test_complexity_many_args():
    """Cover line 162 — field with >5 args."""
    from agent.analyzer import TypeInfo, FieldInfo, find_complexity_issues
    f = FieldInfo(name="search", field_type="String", args=["a","b","c","d","e","f"])
    t = TypeInfo(name="Query", kind="type", fields=[f])
    issues = find_complexity_issues([t])
    assert any("6 args" in i for i in issues)

def test_complexity_many_enum_values():
    """Cover line 164 — enum with >20 values."""
    from agent.analyzer import TypeInfo, find_complexity_issues
    t = TypeInfo(name="Country", kind="enum", values=[f"C{i}" for i in range(25)])
    issues = find_complexity_issues([t])
    assert any("25 values" in i for i in issues)

def test_format_with_issues():
    """Cover lines 180-183 — format_analysis_markdown when issues exist."""
    from agent.analyzer import TypeInfo, FieldInfo
    fields = [FieldInfo(name=f"f{i}", field_type="String") for i in range(25)]
    t = TypeInfo(name="Huge", kind="type", fields=fields)
    types_with_issues = [t]
    stats = get_schema_stats(types_with_issues)
    md = format_analysis_markdown(types_with_issues, stats)
    assert "Issues" in md
    assert "25 fields" in md

def test_to_dict_with_values():
    """Cover line 32: to_dict with values set (enum)."""
    from agent.analyzer import TypeInfo
    t = TypeInfo(name="Status", kind="enum", values=["ACTIVE", "INACTIVE"])
    d = t.to_dict()
    assert "values" in d
    assert d["values"] == ["ACTIVE", "INACTIVE"]
