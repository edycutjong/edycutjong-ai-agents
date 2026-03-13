import pytest
from agent.parser import FigmaParser

def test_corner_radius_uniform():
    node = {"cornerRadius": 8}
    parser = FigmaParser({})
    styles = parser._extract_corner_radius(node)
    assert styles["border-radius"] == "8px"

def test_corner_radius_individual():
    node = {"rectangleCornerRadii": [10, 20, 30, 40]}
    parser = FigmaParser({})
    styles = parser._extract_corner_radius(node)
    assert styles["border-radius"] == "10px 20px 30px 40px"

def test_corner_radius_both():
    node = {"cornerRadius": 8, "rectangleCornerRadii": [10, 20, 30, 40]}
    parser = FigmaParser({})
    styles = parser._extract_corner_radius(node)
    assert styles["border-radius"] == "10px 20px 30px 40px"
