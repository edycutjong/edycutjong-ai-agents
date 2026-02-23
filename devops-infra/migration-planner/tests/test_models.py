import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agent.models import MigrationPlan, MigrationStep

def test_migration_plan_model():
    step = MigrationStep(
        id=1,
        description="Create user table",
        sql_up="CREATE TABLE users (id INT);",
        sql_down="DROP TABLE users;",
        risk_level="low",
        estimated_duration_seconds=10
    )
    plan = MigrationPlan(
        steps=[step],
        summary="Initial migration"
    )
    assert plan.total_estimated_duration_seconds == 0
    assert len(plan.steps) == 1
    assert plan.steps[0].id == 1
