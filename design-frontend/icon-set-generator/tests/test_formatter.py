import pytest
from agent.formatter import IconFormatter

@pytest.fixture
def formatter():
    return IconFormatter()

def test_to_react_component(formatter):
    svg = '<svg stroke-width="2" class="my-icon"><path d="M10 10" /></svg>'
    component = formatter.to_react_component(svg, "TestIcon")

    assert "import React from 'react';" in component
    assert "const TestIcon = (props) => {" in component
    assert "strokeWidth=" in component
    assert "className=" in component
    assert "export default TestIcon;" in component

def test_to_vue_component(formatter):
    svg = '<svg><path d="M10 10" /></svg>'
    component = formatter.to_vue_component(svg, "TestIcon")

    assert "<template>" in component
    assert "<script>" in component
    assert "name: 'TestIcon'" in component

def test_create_sprite_sheet(formatter):
    icons = {
        "icon1": '<svg viewBox="0 0 24 24"><path d="M10 10" /></svg>',
        "icon2": '<svg viewBox="0 0 48 48"><circle r="10" /></svg>'
    }
    sprite = formatter.create_sprite_sheet(icons)

    assert '<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">' in sprite
    assert '<symbol id="icon1" viewBox="0 0 24 24">' in sprite
    assert '<path d="M10 10" />' in sprite
    assert '<symbol id="icon2" viewBox="0 0 48 48">' in sprite
