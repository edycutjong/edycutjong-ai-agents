from typing import List, Dict, Any, Union

class CSSGenerator:
    """Generates CSS code from parsed Figma properties."""

    def __init__(self, processed_nodes: List[Dict[str, Any]]):
        self.nodes = processed_nodes

    def generate_css(self) -> str:
        """Generates standard CSS."""
        css_output = []
        root_vars = self._generate_root_variables()
        if root_vars:
            css_output.append(":root {")
            css_output.extend([f"  {k}: {v};" for k, v in root_vars.items()])
            css_output.append("}\n")

        for node in self.nodes:
            css_class = self._generate_css_class(node)
            if css_class:
                css_output.append(css_class)

        return "\n".join(css_output)

    def generate_scss(self) -> str:
        """Generates SCSS."""
        # For now, simple SCSS (similar to CSS but potentially nested if we implemented hierarchy)
        # We can utilize SCSS variables.
        scss_output = []
        root_vars = self._generate_root_variables()
        if root_vars:
             # SCSS variables
            for k, v in root_vars.items():
                scss_var = k.replace("--", "$")
                scss_output.append(f"{scss_var}: {v};")
            scss_output.append("")

        for node in self.nodes:
             # Basic implementation: same as CSS but could use mixins
            css_class = self._generate_css_class(node, is_scss=True)
            if css_class:
                scss_output.append(css_class)

        return "\n".join(scss_output)

    def generate_css_in_js(self) -> str:
        """Generates CSS-in-JS object syntax."""
        js_output = []
        for node in self.nodes:
            name = self._sanitize_name(node.get("name", "unnamed"))
            # Convert kebab-case-ish name to CamelCase/PascalCase for valid JS identifier
            js_name = self._kebab_to_camel(name)

            styles = {**node.get("styles", {}), **node.get("layout", {})}
            if not styles:
                continue

            js_obj = f"export const {js_name} = {{\n"
            for k, v in styles.items():
                js_key = self._kebab_to_camel(k)
                js_obj += f"  {js_key}: '{v}',\n"
            js_obj += "};\n"
            js_output.append(js_obj)

        return "\n".join(js_output)

    def _generate_root_variables(self) -> Dict[str, str]:
        """Collects unique colors/fonts as variables (simplified logic)."""
        # In a real app, this would aggregate colors from all nodes
        # For now, we return a placeholder or iterate if needed.
        # This implementation simply skips variable extraction for individual nodes
        # to keep 1:1 mapping, but ideally we'd extract common values.
        return {}

    def _generate_css_class(self, node: Dict[str, Any], is_scss: bool = False) -> str:
        """Generates a CSS class block for a node."""
        name = self._sanitize_name(node.get("name", "unnamed"))
        styles = {**node.get("styles", {}), **node.get("layout", {})}

        if not styles:
            return ""

        class_def = f".{name} {{\n"
        for prop, value in styles.items():
             class_def += f"  {prop}: {value};\n"
        class_def += "}\n"

        return class_def

    def _sanitize_name(self, name: str) -> str:
        """Sanitizes Figma node name to be a valid CSS class / JS variable."""
        # Remove invalid chars, replace spaces with hyphens
        safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in name)
        # Ensure it doesn't start with a number
        if safe_name[0].isdigit():
            safe_name = f"class-{safe_name}"
        return safe_name

    def _kebab_to_camel(self, kebab_str: str) -> str:
        """Converts kebab-case to camelCase."""
        parts = kebab_str.split("-")
        return parts[0] + "".join(word.capitalize() for word in parts[1:])
