import pytest
from agent.optimizer import IconOptimizer

@pytest.fixture
def optimizer():
    return IconOptimizer()

def test_optimize_svg_basic(optimizer):
    raw_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px">
        <!-- Comment -->
        <metadata>Meta</metadata>
        <path d="M10 10" />
    </svg>
    """
    optimized = optimizer.optimize_svg(raw_svg)

    # Comments removed
    assert "<!-- Comment -->" not in optimized
    # Metadata removed
    assert "<metadata>" not in optimized
    # ViewBox added/fixed
    assert 'viewBox="0 0 24 24"' in optimized
    # Content preserved
    assert '<path d="M10 10"/>' in optimized or '<path d="M10 10" />' in optimized

def test_optimize_svg_missing_viewbox(optimizer):
    raw_svg = '<svg width="48" height="48"><circle r="10"/></svg>'
    optimized = optimizer.optimize_svg(raw_svg)

    assert 'viewBox="0 0 48 48"' in optimized
    # It keeps original width if present
    assert 'width="48"' in optimized
    # Our implementation sets width="24" if missing, but if present it uses it?
    # Wait, check code:
    # if 'viewBox' not in root.attrib: ... set from width/height
    # if 'width' not in root.attrib: set to 24

    # In this test case, width is 48. So it stays 48?
    # No, code says: if 'width' not in root.attrib -> set "24".
    # Since it is present ("48"), it stays "48".
    pass

def test_optimize_svg_invalid(optimizer):
    raw = "Not an SVG"
    # Should return original or empty? Code catches exception and prints error, returns original.
    result = optimizer.optimize_svg(raw)
    assert result == raw
