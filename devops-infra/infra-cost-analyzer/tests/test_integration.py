import pytest
import pandas as pd
from agent.llm_agent import FinOpsAgent
from agent.analyzer import CostAnalyzer
from agent.recommender import Recommender

def test_full_analysis_pipeline():
    # 1. Create Data
    data = pd.DataFrame({
        'Service': ['EC2', 'EC2', 'ElasticIP'],
        'ResourceID': ['i-high', 'i-low', 'eip-unused'],
        'Cost': [100.0, 100.0, 10.0],
        'CPUUtilization': [80.0, 2.0, 0.0],
        'Date': pd.to_datetime(['2023-01-01']*3),
        'InstanceType': ['m5.large', 'm5.large', 'N/A']
    })

    # 2. Analyze
    analyzer = CostAnalyzer(data)
    total_cost = analyzer.calculate_total_cost()
    waste_df = analyzer.identify_potential_waste()
    top_services = analyzer.calculate_cost_by_service()

    assert total_cost == 210.0
    assert len(waste_df) >= 2 # i-low and eip-unused

    # 3. Recommend
    recommender = Recommender(waste_df)
    right_sizing = recommender.suggest_right_sizing()
    savings = recommender.calculate_total_potential_savings()

    # Expect savings from i-low (40% of 100 = 40) + eip-unused (10) = 50
    assert savings == 50.0

    # 4. Agent Report (Mock)
    # Ensure OPENAI_API_KEY is not set or handle mocked env
    agent = FinOpsAgent()
    # Force mock mode for test stability and to avoid API calls
    agent.is_mock = True

    report = agent.generate_report(
        total_cost=total_cost,
        currency="USD",
        top_services=top_services,
        waste_df=waste_df,
        right_sizing_df=right_sizing,
        potential_savings=savings
    )

    assert "Executive Summary" in report
    assert "USD 210.00" in report
