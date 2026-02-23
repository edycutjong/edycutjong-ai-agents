import pytest
from agent.generator import CSSGenerator

@pytest.fixture
def sample_nodes():
    return [
        {
            "name": "My Button",
            "type": "FRAME",
            "styles": {
                "background-color": "rgba(51, 102, 204, 1.00)",
                "border-radius": "8px"
            },
            "layout": {
                "display": "flex",
                "justify-content": "center"
            }
        },
        {
            "name": "Label",
            "type": "TEXT",
            "styles": {
                "font-size": "16px",
                "color": "#ffffff"
            }
        }
    ]

def test_generate_css(sample_nodes):
    generator = CSSGenerator(sample_nodes)
    css = generator.generate_css()

    assert ".My-Button" in css
    assert "background-color: rgba(51, 102, 204, 1.00);" in css
    assert "display: flex;" in css

    assert ".Label" in css
    assert "font-size: 16px;" in css

def test_generate_scss(sample_nodes):
    generator = CSSGenerator(sample_nodes)
    scss = generator.generate_scss()

    assert ".My-Button" in scss
    # SCSS generation logic is currently simple, same structure
    assert "background-color: rgba(51, 102, 204, 1.00);" in scss

def test_generate_css_in_js(sample_nodes):
    generator = CSSGenerator(sample_nodes)
    js = generator.generate_css_in_js()

    assert "export const MyButton = {" in js
    assert "backgroundColor: 'rgba(51, 102, 204, 1.00)'," in js
    assert "borderRadius: '8px'," in js

    assert "export const Label = {" in js
    assert "fontSize: '16px'," in js
