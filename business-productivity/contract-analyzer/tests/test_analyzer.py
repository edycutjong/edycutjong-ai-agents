"""Tests for Contract Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import analyze_contract, format_analysis_markdown

SAMPLE_CONTRACT = """
SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of January 15, 2026,
by and between "Acme Corporation" (the "Company") and "Client LLC" (the "Client").

1. PAYMENT TERMS
The Client shall pay invoices within Net 30 days of receipt.

2. CONFIDENTIALITY
Both parties agree to maintain the confidentiality of all proprietary information
exchanged under this Agreement. This constitutes a non-disclosure obligation.

3. TERMINATION
Either party may terminate this Agreement with 30 days written notice.
Early termination will incur a termination fee of $5,000.

4. LIABILITY
The Company's total liability shall not exceed the total fees paid.
The Company provides services "as-is" with no warranty disclaimer.
The Client agrees to indemnification of the Company against all claims.

5. NON-COMPETE
The Client agrees to a non-compete clause for a period of 12 months
within a 50-mile radius.

6. INTELLECTUAL PROPERTY
All intellectual property created during the engagement shall remain
the exclusive property of the Company under a perpetual license.

7. DISPUTE RESOLUTION
Any disputes shall be resolved through arbitration in New York, NY,
governed under the governing law of the State of New York.

8. AUTO-RENEWAL
This agreement shall auto-renew annually unless terminated with 60 days notice.

Effective Date: 2026-01-15
Expiration Date: 2027-01-15
"""

# --- Basic Analysis ---
def test_word_count():
    r = analyze_contract(SAMPLE_CONTRACT)
    assert r.word_count > 100

def test_read_time():
    r = analyze_contract(SAMPLE_CONTRACT)
    assert r.estimated_read_time >= 1

# --- Date Extraction ---
def test_dates_extracted():
    r = analyze_contract(SAMPLE_CONTRACT)
    assert len(r.dates) >= 1

# --- Clause Detection ---
def test_payment_clause():
    r = analyze_contract(SAMPLE_CONTRACT)
    types = [c.clause_type for c in r.clauses]
    assert "Payment Terms" in types

def test_confidentiality_clause():
    r = analyze_contract(SAMPLE_CONTRACT)
    types = [c.clause_type for c in r.clauses]
    assert "Confidentiality" in types

def test_termination_clause():
    r = analyze_contract(SAMPLE_CONTRACT)
    types = [c.clause_type for c in r.clauses]
    assert "Termination" in types

def test_liability_clause():
    r = analyze_contract(SAMPLE_CONTRACT)
    types = [c.clause_type for c in r.clauses]
    assert "Liability" in types

def test_ip_clause():
    r = analyze_contract(SAMPLE_CONTRACT)
    types = [c.clause_type for c in r.clauses]
    assert "Intellectual Property" in types

def test_dispute_clause():
    r = analyze_contract(SAMPLE_CONTRACT)
    types = [c.clause_type for c in r.clauses]
    assert "Dispute Resolution" in types

def test_noncompete_clause():
    r = analyze_contract(SAMPLE_CONTRACT)
    types = [c.clause_type for c in r.clauses]
    assert "Non-Compete" in types

# --- Risk Detection ---
def test_high_risks_detected():
    r = analyze_contract(SAMPLE_CONTRACT)
    assert r.high_risks >= 2  # indemnification, non-compete, auto-renew, perpetual license

def test_medium_risks_detected():
    r = analyze_contract(SAMPLE_CONTRACT)
    medium = [ri for ri in r.risks if ri.severity == "medium"]
    assert len(medium) >= 2

def test_risk_score():
    r = analyze_contract(SAMPLE_CONTRACT)
    assert r.risk_score > 0

def test_risk_has_recommendation():
    r = analyze_contract(SAMPLE_CONTRACT)
    recs = [ri for ri in r.risks if ri.recommendation]
    assert len(recs) >= 1

# --- Formatting ---
def test_markdown_format():
    r = analyze_contract(SAMPLE_CONTRACT)
    md = format_analysis_markdown(r)
    assert "Contract Analysis" in md
    assert "Risk Score" in md

def test_to_dict():
    r = analyze_contract(SAMPLE_CONTRACT)
    d = r.to_dict()
    assert "risk_score" in d
    assert "clauses" in d
    assert "risks" in d

# --- Edge Cases ---
def test_empty_contract():
    r = analyze_contract("")
    assert r.word_count == 0
    assert len(r.risks) == 0

def test_short_contract():
    r = analyze_contract("This is a simple agreement between two parties.")
    assert r.word_count > 0
