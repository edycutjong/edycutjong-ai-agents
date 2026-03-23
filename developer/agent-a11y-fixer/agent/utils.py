from bs4 import BeautifulSoup
import re

def parse_html(html_string):
    """Parse HTML string into BeautifulSoup object."""
    return BeautifulSoup(html_string, 'html.parser')

def calculate_luminance(hex_color):
    """Calculate relative luminance for WCAG contrast ratio."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    
    def process_channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = process_channel(r), process_channel(g), process_channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(hex1, hex2):
    """Calculate WCAG contrast ratio between two hex colors."""
    lum1 = calculate_luminance(hex1)
    lum2 = calculate_luminance(hex2)
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return (brightest + 0.05) / (darkest + 0.05)

def analyze_contrast(bg_color, fg_color):
    """Check if color contrast passes WCAG AA (4.5:1 for normal text)."""
    ratio = contrast_ratio(bg_color, fg_color)
    return {
        "ratio": round(ratio, 2),
        "passes_aa": ratio >= 4.5,
        "passes_aaa": ratio >= 7.0
    }

def generate_audit_report(issues, filename="a11y_report.html"):
    """Generate an HTML accessibility audit report following design guidelines."""
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A11y Audit Report</title>
    <style>
        body {{
            background-color: #0A1022;
            color: #E2E8F0;
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 2rem;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        h1 {{
            color: #3B82F6;
            margin-top: 0;
        }}
        .issue {{
            background-color: rgba(245, 158, 11, 0.1);
            border-left: 4px solid #F59E0B;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0 8px 8px 0;
        }}
        .issue-title {{
            color: #F59E0B;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        code {{
            background-color: rgba(0,0,0,0.5);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            color: #60A5FA;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Accessibility Audit Report</h1>
        <p>Found <strong>{len(issues)}</strong> potential issues.</p>
        <div class="issues-list">
'''
    if not issues:
        html_content += '<p>No issues found! Great job!</p>'
    else:
        for issue in issues:
            html_content += f'''
            <div class="issue">
                <div class="issue-title">{issue.get("type", "Issue")}</div>
                <div class="issue-desc">{issue.get("description", "")}</div>
                <div><code>{issue.get("element", "")}</code></div>
                <div><strong>Recommendation:</strong> {issue.get("recommendation", "")}</div>
            </div>
            '''
    
    html_content += '''
        </div>
    </div>
</body>
</html>
'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return filename
