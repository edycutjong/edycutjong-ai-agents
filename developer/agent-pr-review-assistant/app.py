"""PR Review Assistant – Streamlit Agent.

Paste a GitHub PR URL to get a structured code review with
severity badges and actionable suggestions.
"""

import re
import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="PR Review Assistant", page_icon="🔍", layout="wide")

# ── Styles ───────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .badge-critical{background:#ef4444;color:#fff;padding:2px 8px;border-radius:4px;font-size:.8rem;font-weight:600}
    .badge-warning{background:#f59e0b;color:#000;padding:2px 8px;border-radius:4px;font-size:.8rem;font-weight:600}
    .badge-info{background:#3b82f6;color:#fff;padding:2px 8px;border-radius:4px;font-size:.8rem;font-weight:600}
    .review-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin:12px 0}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Constants ────────────────────────────────────────────────
GITHUB_API = "https://api.github.com"
PR_URL_RE = re.compile(
    r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)"
)

SECURITY_PATTERNS = [
    (r"(?i)password\s*=\s*['\"]", "Possible hardcoded password"),
    (r"(?i)api[_-]?key\s*=\s*['\"]", "Possible hardcoded API key"),
    (r"(?i)secret\s*=\s*['\"]", "Possible hardcoded secret"),
    (r"eval\s*\(", "Use of eval()"),
    (r"exec\s*\(", "Use of exec()"),
    (r"(?i)token\s*=\s*['\"]", "Possible hardcoded token"),
]

# ── Helpers ──────────────────────────────────────────────────


def parse_pr_url(url: str) -> dict | None:
    """Extract owner, repo, and PR number from a GitHub PR URL."""
    m = PR_URL_RE.match(url.strip())
    if not m:
        return None
    return {
        "owner": m.group("owner"),
        "repo": m.group("repo"),
        "number": int(m.group("number")),
    }


def fetch_pr_info(owner: str, repo: str, number: int, token: str | None = None):
    """Return PR metadata dict from the GitHub API."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_pr_files(owner: str, repo: str, number: int, token: str | None = None):
    """Return the list of changed files (with patches) for a PR."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}/files"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


# ── Analysis functions ───────────────────────────────────────


def _badge(severity: str, text: str) -> str:
    return f'<span class="badge-{severity}">{text.upper()}</span>'


def analyse_file(file_info: dict) -> list[dict]:
    """Run heuristic checks on a single file's patch."""
    findings: list[dict] = []
    patch = file_info.get("patch", "")
    filename = file_info.get("filename", "")
    additions = file_info.get("additions", 0)

    # ── Large file change ────────────────────────────────
    if additions > 300:
        findings.append(
            {
                "severity": "warning",
                "title": "Large change",
                "detail": f"`{filename}` has **{additions}** additions — consider splitting.",
            }
        )

    # ── TODO / FIXME / HACK ──────────────────────────────
    for line in patch.splitlines():
        if line.startswith("+") and re.search(r"\b(TODO|FIXME|HACK|XXX)\b", line):
            findings.append(
                {
                    "severity": "info",
                    "title": "TODO/FIXME detected",
                    "detail": f"`{filename}`: `{line.strip()[:120]}`",
                }
            )

    # ── Security patterns ────────────────────────────────
    for pattern, message in SECURITY_PATTERNS:
        for line in patch.splitlines():
            if line.startswith("+") and re.search(pattern, line):
                findings.append(
                    {
                        "severity": "critical",
                        "title": message,
                        "detail": f"`{filename}`: `{line.strip()[:120]}`",
                    }
                )

    # ── Missing tests heuristic ──────────────────────────
    if (
        filename.endswith((".py", ".ts", ".js", ".go", ".rs"))
        and "test" not in filename.lower()
    ):
        findings.append(
            {
                "severity": "info",
                "title": "No companion test file detected",
                "detail": f"Consider adding tests for `{filename}`.",
            }
        )

    # ── Hardcoded values (IPs, URLs) ─────────────────────
    for line in patch.splitlines():
        if line.startswith("+"):
            if re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line):
                findings.append(
                    {
                        "severity": "warning",
                        "title": "Hardcoded IP detected",
                        "detail": f"`{filename}`: `{line.strip()[:120]}`",
                    }
                )

    return findings


def build_review(pr_info: dict, files: list[dict]) -> tuple[list[dict], str]:
    """Run analysis on all files and return (findings, markdown_comment)."""
    all_findings: list[dict] = []
    for f in files:
        all_findings.extend(analyse_file(f))

    # Build markdown comment
    lines = [
        f"## 🔍 PR Review: #{pr_info['number']} — {pr_info['title']}",
        "",
        f"**Author:** {pr_info['user']['login']}  ",
        f"**Changed files:** {len(files)}  ",
        f"**Findings:** {len(all_findings)}",
        "",
    ]

    severity_order = {"critical": 0, "warning": 1, "info": 2}
    sorted_findings = sorted(
        all_findings, key=lambda f: severity_order.get(f["severity"], 9)
    )

    if sorted_findings:
        lines.append("### Findings\n")
        for finding in sorted_findings:
            icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(
                finding["severity"], "⚪"
            )
            lines.append(
                f"- {icon} **[{finding['severity'].upper()}]** {finding['title']}  "
            )
            lines.append(f"  {finding['detail']}")
            lines.append("")
    else:
        lines.append("✅ No issues found — looks good!")

    return all_findings, "\n".join(lines)


# ── UI ───────────────────────────────────────────────────────

st.title("🔍 PR Review Assistant")
st.caption("Paste a GitHub PR URL to get a structured code review.")

with st.sidebar:
    st.header("⚙️ Settings")
    github_token = st.text_input(
        "GitHub Token (optional)",
        type="password",
        help="Required for private repos or to raise API rate limits.",
    )

pr_url = st.text_input(
    "GitHub PR URL",
    placeholder="https://github.com/owner/repo/pull/123",
)

if st.button("🚀 Run Review", type="primary", use_container_width=True):
    if not pr_url:
        st.error("Please enter a PR URL.")
    else:
        parsed = parse_pr_url(pr_url)
        if parsed is None:
            st.error("Invalid GitHub PR URL. Expected format: `https://github.com/owner/repo/pull/123`")
        else:
            token = github_token or None
            with st.spinner("Fetching PR data from GitHub…"):
                try:
                    pr_info = fetch_pr_info(parsed["owner"], parsed["repo"], parsed["number"], token)
                    files = fetch_pr_files(parsed["owner"], parsed["repo"], parsed["number"], token)
                except requests.HTTPError as exc:
                    st.error(f"GitHub API error: {exc.response.status_code} — {exc.response.reason}")
                    st.stop()

            with st.spinner("Analysing changes…"):
                findings, md_comment = build_review(pr_info, files)

            # ── Summary ──────────────────────────────────────
            c1, c2, c3 = st.columns(3)
            critical = sum(1 for f in findings if f["severity"] == "critical")
            warnings = sum(1 for f in findings if f["severity"] == "warning")
            infos = sum(1 for f in findings if f["severity"] == "info")
            c1.metric("🔴 Critical", critical)
            c2.metric("🟡 Warnings", warnings)
            c3.metric("🔵 Info", infos)

            st.divider()

            # ── Findings ─────────────────────────────────────
            for finding in sorted(findings, key=lambda x: {"critical": 0, "warning": 1, "info": 2}.get(x["severity"], 9)):
                badge_html = _badge(finding["severity"], finding["severity"])
                st.markdown(
                    f'<div class="review-card">{badge_html} <strong>{finding["title"]}</strong><br/>{finding["detail"]}</div>',
                    unsafe_allow_html=True,
                )

            if not findings:
                st.success("✅ No issues found — this PR looks clean!")

            st.divider()

            # ── Copy as Markdown ─────────────────────────────
            st.subheader("📋 Markdown Comment")
            st.code(md_comment, language="markdown")
