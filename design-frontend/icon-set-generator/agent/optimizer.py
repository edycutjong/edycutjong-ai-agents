from lxml import etree
import re

class IconOptimizer:
    def optimize_svg(self, svg_content: str) -> str:
        """
        Optimizes SVG content by:
        - Removing comments
        - Removing metadata
        - Ensuring viewBox is present
        - Minifying whitespace (basic)
        """
        if not svg_content:
            return ""

        try:
            # Parse XML
            parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
            root = etree.fromstring(svg_content.encode('utf-8'), parser)

            # Remove namespaces if not needed, but SVG needs xmlns usually.
            # We keep standard SVG namespaces.

            # Remove metadata tags
            for elem in root.xpath('//*[local-name()="metadata" or local-name()="title" or local-name()="desc"]'):
                elem.getparent().remove(elem)

            # Ensure attributes
            if 'viewBox' not in root.attrib:
                width = root.attrib.get('width', '24').replace('px', '')
                height = root.attrib.get('height', '24').replace('px', '')
                root.attrib['viewBox'] = f"0 0 {width} {height}"

            # Standardize width/height if missing
            if 'width' not in root.attrib:
                root.attrib['width'] = "24"
            if 'height' not in root.attrib:
                root.attrib['height'] = "24"

            # Serialize to string
            optimized_svg = etree.tostring(root, encoding='unicode', pretty_print=False)

            # Remove XML declaration if present (<?xml ... ?>)
            if optimized_svg.startswith("<?xml"):
                optimized_svg = re.sub(r'<\?xml.*?\?>', '', optimized_svg, count=1)

            return optimized_svg.strip()

        except Exception as e:
            # Fallback to original content if optimization fails
            print(f"Optimization failed: {e}")
            return svg_content
