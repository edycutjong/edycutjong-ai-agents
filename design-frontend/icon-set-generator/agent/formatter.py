import re
from typing import List, Dict

class IconFormatter:
    def to_react_component(self, svg_content: str, component_name: str) -> str:
        """Converts SVG string to a React component."""

        # Convert attributes to camelCase
        # e.g., stroke-width -> strokeWidth
        def to_camel_case(match):
            return match.group(1) + match.group(2).upper()

        react_svg = re.sub(r'([a-z]+)-([a-z])', to_camel_case, svg_content)

        # Replace class with className
        react_svg = react_svg.replace('class=', 'className=')

        # Ensure styles are objects if present (simple check)
        # Usually SVGs from LLM don't have style="..." with CSS string, but if they do, React needs object.
        # We'll assume standard SVG attributes for now.

        component = f"""import React from 'react';

const {component_name} = (props) => {{
  return (
    {react_svg.replace('<svg', '<svg {...props}')}
  );
}};

export default {component_name};
"""
        return component

    def to_vue_component(self, svg_content: str, component_name: str) -> str:
        """Converts SVG string to a Vue component."""
        # Vue handles standard SVG attributes fine.
        # We just need to wrap it.

        component = f"""<template>
  {svg_content}
</template>

<script>
export default {{
  name: '{component_name}'
}}
</script>
"""
        return component

    def create_sprite_sheet(self, icons: Dict[str, str]) -> str:
        """
        Creates an SVG sprite sheet from a dictionary of {name: svg_content}.
        """
        symbols = []
        for name, svg in icons.items():
            # Extract content inside <svg>...</svg>
            content_match = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.DOTALL)
            if content_match:
                content = content_match.group(1)
                # Parse viewBox from original svg tag
                viewbox_match = re.search(r'viewBox="([^"]*)"', svg)
                viewbox = viewbox_match.group(1) if viewbox_match else "0 0 24 24"

                symbol = f'<symbol id="{name}" viewBox="{viewbox}">\n{content}\n</symbol>'
                symbols.append(symbol)
            else:
                # Fallback if regex fails (e.g. malformed or different structure)
                # Try to wrap entire svg in symbol? No, nested svgs are valid but symbol is better.
                pass

        sprite = f"""<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
{''.join(symbols)}
</svg>"""
        return sprite
