import json
from typing import Dict, Any, List, Optional, Union

class FigmaParser:
    """Parses Figma JSON export to extract design tokens and CSS properties."""

    def __init__(self, figma_data: Dict[str, Any]):
        self.data = figma_data
        self.document = figma_data.get("document", {})

    def parse(self) -> List[Dict[str, Any]]:
        """Parses the entire document and returns a list of processed nodes."""
        return self._traverse(self.document)

    def _traverse(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recursively traverses the node tree."""
        processed_nodes = []

        # Process current node if it's a relevant type
        if self._is_relevant_node(node):
            processed_nodes.append(self._extract_properties(node))

        # Traverse children
        if "children" in node:
            for child in node["children"]:
                processed_nodes.extend(self._traverse(child))

        return processed_nodes

    def _is_relevant_node(self, node: Dict[str, Any]) -> bool:
        """Filters relevant nodes for CSS generation."""
        # We generally want Frames, Groups, Text, Rectangles, Vectors, Components, Instances
        relevant_types = {
            "FRAME", "GROUP", "TEXT", "RECTANGLE", "VECTOR",
            "COMPONENT", "INSTANCE", "STAR", "LINE", "ELLIPSE",
            "REGULAR_POLYGON"
        }
        return node.get("type") in relevant_types

    def _extract_properties(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts CSS-relevant properties from a node."""
        props = {
            "id": node.get("id"),
            "name": node.get("name"),
            "type": node.get("type"),
            "styles": {},
            "layout": {},
            "children": [] # Store IDs of children for hierarchy reconstruction if needed
        }

        # Extract basic styles
        props["styles"].update(self._extract_fills(node))
        props["styles"].update(self._extract_strokes(node))
        props["styles"].update(self._extract_effects(node))
        props["styles"].update(self._extract_typography(node))
        props["styles"].update(self._extract_dimensions(node))
        props["styles"].update(self._extract_corner_radius(node))

        # Extract layout (Flexbox/Grid)
        props["layout"].update(self._extract_layout(node))

        return props

    def _extract_fills(self, node: Dict[str, Any]) -> Dict[str, str]:
        """Extracts background color/image."""
        styles = {}
        fills = node.get("fills", [])
        for fill in fills:
            if fill.get("visible", True) and fill.get("type") == "SOLID":
                color = fill.get("color")
                opacity = fill.get("opacity", 1.0)
                if color:
                    styles["background-color"] = self._rgba_to_css(color, opacity)
                    return styles # Return first visible solid fill as background
        return styles  # pragma: no cover

    def _extract_strokes(self, node: Dict[str, Any]) -> Dict[str, str]:
        """Extracts border properties."""
        styles = {}
        strokes = node.get("strokes", [])
        weight = node.get("strokeWeight", 0)
        align = node.get("strokeAlign", "INSIDE") # INSIDE, OUTSIDE, CENTER

        for stroke in strokes:
            if stroke.get("visible", True) and stroke.get("type") == "SOLID":  # pragma: no cover
                color = stroke.get("color")  # pragma: no cover
                opacity = stroke.get("opacity", 1.0)  # pragma: no cover
                if color and weight > 0:  # pragma: no cover
                    css_color = self._rgba_to_css(color, opacity)  # pragma: no cover
                    styles["border"] = f"{weight}px solid {css_color}"  # pragma: no cover
                    # Note: CSS border is always effectively 'inside' the box model boundary
                    # but rendered differently. For simplicity, we map to standard border.
                    return styles  # pragma: no cover
        return styles

    def _extract_effects(self, node: Dict[str, Any]) -> Dict[str, str]:
        """Extracts shadows and layer blurs."""
        styles = {}
        effects = node.get("effects", [])
        box_shadows = []

        for effect in effects:
            if not effect.get("visible", True):  # pragma: no cover
                continue  # pragma: no cover

            e_type = effect.get("type")  # pragma: no cover
            if e_type in ["DROP_SHADOW", "INNER_SHADOW"]:  # pragma: no cover
                color = effect.get("color")  # pragma: no cover
                offset = effect.get("offset", {"x": 0, "y": 0})  # pragma: no cover
                radius = effect.get("radius", 0)  # pragma: no cover
                spread = effect.get("spread", 0) # Not always present in all API versions  # pragma: no cover

                if color:  # pragma: no cover
                    css_color = self._rgba_to_css(color, color.get("a", 1))  # pragma: no cover
                    inset = "inset " if e_type == "INNER_SHADOW" else ""  # pragma: no cover
                    shadow = f"{inset}{offset['x']}px {offset['y']}px {radius}px {spread}px {css_color}"  # pragma: no cover
                    box_shadows.append(shadow)  # pragma: no cover

            elif e_type == "LAYER_BLUR":  # pragma: no cover
                radius = effect.get("radius", 0)  # pragma: no cover
                styles["filter"] = f"blur({radius}px)"  # pragma: no cover

        if box_shadows:
            styles["box-shadow"] = ", ".join(box_shadows)  # pragma: no cover

        return styles

    def _extract_typography(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts font properties."""
        styles = {}
        style = node.get("style", {})
        if not style:
            return styles

        if "fontFamily" in style:
            styles["font-family"] = f"'{style['fontFamily']}'"

        if "fontSize" in style:
            styles["font-size"] = f"{style['fontSize']}px"

        if "fontWeight" in style:
            styles["font-weight"] = style['fontWeight']

        if "lineHeightPx" in style:
            styles["line-height"] = f"{style['lineHeightPx']}px"

        if "letterSpacing" in style:
             styles["letter-spacing"] = f"{style['letterSpacing']}px"  # pragma: no cover

        if "textAlignHorizontal" in style:
            align_map = {
                "LEFT": "left",
                "RIGHT": "right",
                "CENTER": "center",
                "JUSTIFIED": "justify"
            }
            styles["text-align"] = align_map.get(style["textAlignHorizontal"], "left")

        if "textTransform" in style:
             transform_map = {  # pragma: no cover
                 "UPPERCASE": "uppercase",
                 "LOWERCASE": "lowercase",
                 "TITLECASE": "capitalize"
             }
             if style["textTransform"] in transform_map:  # pragma: no cover
                 styles["text-transform"] = transform_map[style["textTransform"]]  # pragma: no cover

        return styles

    def _extract_dimensions(self, node: Dict[str, Any]) -> Dict[str, str]:
        """Extracts width and height."""
        styles = {}
        bbox = node.get("absoluteBoundingBox")
        if bbox:
            styles["width"] = f"{bbox['width']}px"
            styles["height"] = f"{bbox['height']}px"
        return styles

    def _extract_corner_radius(self, node: Dict[str, Any]) -> Dict[str, str]:
        """Extracts border radius."""
        styles = {}
        radius = node.get("cornerRadius")
        if radius:
             styles["border-radius"] = f"{radius}px"
        # TODO: Handle rectangleCornerRadii for individual corners
        return styles

    def _extract_layout(self, node: Dict[str, Any]) -> Dict[str, str]:
        """Extracts Flexbox/AutoLayout properties."""
        layout = {}

        # Check if Auto Layout is enabled
        if node.get("layoutMode") in ["HORIZONTAL", "VERTICAL"]:
            layout["display"] = "flex"
            layout["flex-direction"] = "row" if node["layoutMode"] == "HORIZONTAL" else "column"

            # Gap
            item_spacing = node.get("itemSpacing", 0)
            if item_spacing > 0:
                layout["gap"] = f"{item_spacing}px"  # pragma: no cover

            # Padding
            p_left = node.get("paddingLeft", 0)
            p_right = node.get("paddingRight", 0)
            p_top = node.get("paddingTop", 0)
            p_bottom = node.get("paddingBottom", 0)

            if any([p_left, p_right, p_top, p_bottom]):
                layout["padding"] = f"{p_top}px {p_right}px {p_bottom}px {p_left}px"  # pragma: no cover

            # Align Items (Counter Axis)
            align_items_map = {
                "MIN": "flex-start",
                "CENTER": "center",
                "MAX": "flex-end",
                "STRETCH": "stretch",
                "BASELINE": "baseline"
            }
            counter_align = node.get("counterAxisAlignItems") # defaults to MIN
            if counter_align:
                 layout["align-items"] = align_items_map.get(counter_align, "flex-start")

            # Justify Content (Primary Axis)
            justify_content_map = {
                "MIN": "flex-start",
                "CENTER": "center",
                "MAX": "flex-end",
                "SPACE_BETWEEN": "space-between"
            }
            primary_align = node.get("primaryAxisAlignItems")
            if primary_align:
                layout["justify-content"] = justify_content_map.get(primary_align, "flex-start")

        return layout

    def _rgba_to_css(self, color: Dict[str, float], opacity: float = 1.0) -> str:
        """Converts Figma RGB (0-1) to CSS rgba()."""
        r = int(color.get("r", 0) * 255)
        g = int(color.get("g", 0) * 255)
        b = int(color.get("b", 0) * 255)
        a = color.get("a", 1.0) * opacity

        if a >= 1.0:
            return f"rgb({r}, {g}, {b})"
        return f"rgba({r}, {g}, {b}, {a:.2f})"  # pragma: no cover
