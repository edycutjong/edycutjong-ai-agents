from fpdf import FPDF
from .models import Proposal

class ProposalPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, 'Project Proposal', align='R', new_x="LMARGIN", new_y="NEXT")

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def create_pdf(proposal: Proposal, filename: str):
    pdf = ProposalPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 20, proposal.project_title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    # Executive Summary
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, proposal.executive_summary)
    pdf.ln(10)

    # Scope of Work
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Scope of Work", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=12)
    for item in proposal.scope_of_work:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"- {item.title}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 8, item.description)
        pdf.ln(2)
    pdf.ln(5)

    # Timeline
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Timeline", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=12)

    # Table Header
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(40, 10, "Date", border=1)
    pdf.cell(50, 10, "Milestone", border=1)
    pdf.cell(100, 10, "Description", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=11)
    for milestone in proposal.timeline:
        pdf.cell(40, 10, milestone.date, border=1)
        pdf.cell(50, 10, milestone.name, border=1)
        # Handle long description in table cell? MultiCell is tricky in tables.
        # Simplification: truncate or just put it there. FPDF2 has better table support but let's stick to basics or use multi_cell manually.
        # Let's try to fit it.
        # Actually FPDF2 has table context manager.
        pdf.cell(100, 10, milestone.description[:50] + "..." if len(milestone.description) > 50 else milestone.description, border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Budget
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Budget", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=12)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Cost", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=11)
    total_cost = 0.0
    for item in proposal.budget:
        pdf.cell(80, 10, item.item, border=1)
        pdf.cell(30, 10, f"${item.cost:,.2f}", border=1, new_x="LMARGIN", new_y="NEXT")
        total_cost += item.cost

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Total", border=1)
    pdf.cell(30, 10, f"${total_cost:,.2f}", border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Deliverables
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Deliverables", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=12)
    for deliverable in proposal.deliverables:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"- {deliverable.name} ({deliverable.format})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 8, f"Criteria: {deliverable.acceptance_criteria}")
        pdf.ln(2)
    pdf.ln(5)

    # Risks
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Risks", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=12)
    for risk in proposal.risks:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"Risk: {risk.description} (Severity: {risk.severity})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 8, f"Mitigation: {risk.mitigation}")
        pdf.ln(2)

    pdf.output(filename)

def create_markdown(proposal: Proposal, filename: str):
    md = f"# {proposal.project_title}\n\n"

    md += "## Executive Summary\n"
    md += f"{proposal.executive_summary}\n\n"

    md += "## Scope of Work\n"
    for item in proposal.scope_of_work:
        md += f"### {item.title}\n"
        md += f"{item.description}\n\n"

    md += "## Timeline\n"
    md += "| Milestone | Date | Description |\n"
    md += "| --- | --- | --- |\n"
    for m in proposal.timeline:
        md += f"| {m.name} | {m.date} | {m.description} |\n"
    md += "\n"

    md += "## Budget\n"
    md += "| Item | Cost | Description |\n"
    md += "| --- | --- | --- |\n"
    total = 0
    for b in proposal.budget:
        md += f"| {b.item} | ${b.cost:,.2f} | {b.description or ''} |\n"
        total += b.cost
    md += f"| **Total** | **${total:,.2f}** | |\n\n"

    md += "## Deliverables\n"
    for d in proposal.deliverables:
        md += f"- **{d.name}** ({d.format}): {d.acceptance_criteria}\n"
    md += "\n"

    md += "## Risks\n"
    for r in proposal.risks:
        md += f"- **{r.severity} Severity**: {r.description}\n  - Mitigation: {r.mitigation}\n"

    with open(filename, 'w') as f:
        f.write(md)
