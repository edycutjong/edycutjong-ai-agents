import os
import sys
import pytest

# Add project root to sys.path
sys.path.append(os.path.join(os.getcwd(), 'apps/agents/design-frontend/ui-copy-reviewer'))

from agent.extractor import TextExtractor, extract_text_from_file

class TestExtractor:
    @pytest.fixture
    def extractor(self):
        return TextExtractor()

    def test_html_extraction(self, extractor, tmp_path):
        content = '<html><body><h1>Welcome</h1><button title="Click Me">Submit</button></body></html>'
        f = tmp_path / "test.html"
        f.write_text(content, encoding="utf-8")

        results = extractor.extract_text_from_file(str(f))

        assert len(results) == 3
        # Text node
        assert any(r['text'] == 'Welcome' and r['type'] == 'content' for r in results)
        assert any(r['text'] == 'Submit' and r['type'] == 'content' for r in results)
        # Attribute
        assert any(r['text'] == 'Click Me' and r['type'] == 'attribute' for r in results)

    def test_jsx_extraction(self, extractor, tmp_path):
        content = """
        const App = () => {
            return (
                <div className="container">
                    <h1>Hello React</h1>
                    <img src="logo.png" alt="Logo" />
                    <button title="Submit Form">Send</button>
                </div>
            )
        }
        """
        f = tmp_path / "test.jsx"
        f.write_text(content, encoding="utf-8")

        results = extractor.extract_text_from_file(str(f))

        # Expect: "Hello React", "Logo" (alt), "Submit Form" (title), "Send" (text content)
        texts = [r['text'] for r in results]
        assert "Hello React" in texts
        assert "Logo" in texts
        assert "Submit Form" in texts
        assert "Send" in texts

        # Check context
        hello_item = next(r for r in results if r['text'] == "Hello React")
        assert "<h1>Hello React</h1>" in hello_item['context']
        assert hello_item['line'] is not None

    def test_unsupported_file(self, extractor, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Hello World", encoding="utf-8")
        results = extractor.extract_text_from_file(str(f))
        assert results == []

    def test_file_not_found(self, extractor):
        with pytest.raises(FileNotFoundError):
            extractor.extract_text_from_file("non_existent_file.html")
