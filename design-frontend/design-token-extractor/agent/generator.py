import json
from typing import Dict, Any
from .models import TokenSet, DesignToken

class DesignGenerator:
    @staticmethod
    def to_css(token_set: TokenSet) -> str:
        """Generates CSS custom properties."""
        lines = [":root {"]
        for token in token_set.tokens:
            lines.append(f"  --{token.name}: {token.value};")
        lines.append("}")
        return "\n".join(lines)

    @staticmethod
    def to_scss(token_set: TokenSet) -> str:
        """Generates SCSS variables."""
        lines = []
        for token in token_set.tokens:
            lines.append(f"${token.name}: {token.value};")
        return "\n".join(lines)

    @staticmethod
    def to_tailwind(token_set: TokenSet) -> str:
        """Generates a Tailwind CSS configuration (JS format)."""
        theme: Dict[str, Any] = {"extend": {}}

        # Map generic types to Tailwind theme keys
        type_mapping = {
            "color": "colors",
            "spacing": "spacing",
            "typography": "fontSize", # simplified mapping
            "fontSize": "fontSize",
            "fontFamily": "fontFamily",
            "fontWeight": "fontWeight",
            "lineHeight": "lineHeight",
            "borderRadius": "borderRadius",
            "borderWidth": "borderWidth",
            "shadow": "boxShadow",
            "opacity": "opacity",
            "zIndex": "zIndex"
        }

        for token in token_set.tokens:
            tw_key = type_mapping.get(token.type, "misc")

            if tw_key == "misc":
                continue

            if tw_key not in theme["extend"]:
                theme["extend"][tw_key] = {}

            # Use the token name as the key
            # Remove the prefix if it matches the key (e.g., 'color-primary' -> 'primary')
            # But kept simple for now: just use the name
            theme["extend"][tw_key][token.name] = token.value

        return f"module.exports = {{\n  theme: {json.dumps(theme, indent=2)}\n}};"

    @staticmethod
    def to_json(token_set: TokenSet) -> str:
        """Generates W3C Design Tokens Format JSON."""
        output = {}
        for token in token_set.tokens:
            output[token.name] = {
                "$value": token.value,
                "$type": token.type,
                "$description": token.description or ""
            }
        return json.dumps(output, indent=2)
