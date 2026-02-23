from typing import List
from .analyzer import DeprecationFinding

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deprecation Hunter Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Fira+Code&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f0f2f5;
            --card-bg: #ffffff;
            --text-color: #1f2937;
            --primary: #4a90e2;
            --secondary: #50e3c2;
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-size: 3.5rem;
            margin-bottom: 10px;
            font-weight: 800;
            animation: fadeIn 1s ease-in;
        }
        .subtitle {
            text-align: center;
            color: #6b7280;
            margin-bottom: 50px;
            animation: fadeIn 1.2s ease-in;
        }
        .finding-card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s, box-shadow 0.2s;
            animation: slideUp 0.5s ease-out forwards;
            opacity: 0;
            border: 1px solid rgba(0,0,0,0.05);
        }
        .finding-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .file-path {
            font-weight: 600;
            color: #4b5563;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .line-number {
            color: #9ca3af;
            font-weight: normal;
        }
        .code-block {
            background: #fee2e2;
            padding: 16px;
            border-radius: 8px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            border-left: 4px solid #ef4444;
            margin-bottom: 12px;
            color: #991b1b;
        }
        .suggestion-block {
            background: #d1fae5;
            padding: 16px;
            border-radius: 8px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            border-left: 4px solid #10b981;
            color: #065f46;
        }
        .message {
            margin: 12px 0;
            color: #374151;
            line-height: 1.5;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .badge-warning {
            background-color: #fff7ed;
            color: #c2410c;
            border: 1px solid #ffedd5;
        }
        .badge-error {
            background-color: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fee2e2;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Deprecation Hunter</h1>
        <div class="subtitle">Found {count} issues in your codebase</div>
        <div id="findings">
            {content}
        </div>
    </div>
</body>
</html>
"""

def generate_report(findings: List[DeprecationFinding], output_path: str = "deprecation_report.html"):
    content_html = ""
    for i, finding in enumerate(findings):
        delay = i * 0.1
        severity_class = "badge-warning" if finding.severity == "warning" else "badge-error"

        card = f"""
        <div class="finding-card" style="animation-delay: {delay}s">
            <div class="header-row">
                <div class="file-path">
                    {finding.filepath} <span class="line-number">L{finding.line_number}</span>
                </div>
                <span class="badge {severity_class}">{finding.severity}</span>
            </div>
            <div class="code-block">
                {finding.code}
            </div>
            <div class="message">
                {finding.message}
            </div>
            <div class="suggestion-block">
                {finding.suggestion}
            </div>
        </div>
        """
        content_html += card

    final_html = TEMPLATE.replace("{content}", content_html).replace("{count}", str(len(findings)))

    with open(output_path, "w") as f:
        f.write(final_html)

    return output_path
