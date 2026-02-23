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
