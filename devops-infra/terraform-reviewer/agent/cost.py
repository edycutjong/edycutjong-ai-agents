from typing import Dict, Any

PRICING_MAP = {
    "aws_instance": {
        "t2.micro": 8.50,
        "t3.micro": 7.50,
        "t3.small": 15.00,
        "t3.medium": 30.00,
        "m5.large": 70.00,
        "m5.xlarge": 140.00,
        "c5.large": 64.00,
    },
    "aws_db_instance": {
        "db.t3.micro": 12.00,
        "db.t3.small": 24.00,
        "db.m5.large": 100.00,
    },
    "aws_lb": {
        "application": 20.00,  # Base price per ALB
        "network": 20.00
    },
    "aws_nat_gateway": {
        "default": 32.00
    }
}

class CostEstimator:
    def estimate(self, hcl_data: Dict[str, Any]) -> Dict[str, float]:
        total_cost = 0.0
        breakdown = {}

        if not hcl_data or 'resource' not in hcl_data:
            return {"total_monthly_cost": 0.0, "details": {}}

        resources = hcl_data.get('resource', [])
        for resource_block in resources:
            for resource_type, resource_instances in resource_block.items():
                for name, config in resource_instances.items():
                    cost = 0.0

                    if resource_type == "aws_instance":
                        instance_type = config.get("instance_type", "t2.micro") # Default fallback
                        cost = PRICING_MAP["aws_instance"].get(instance_type, 10.00) # Fallback cost

                    elif resource_type == "aws_db_instance":
                        instance_class = config.get("instance_class", "db.t3.micro")
                        cost = PRICING_MAP["aws_db_instance"].get(instance_class, 20.00)

                    elif resource_type == "aws_lb":
                         # Load balancer pricing depends on usage, but base price exists
                         lb_type = config.get("load_balancer_type", "application")
                         cost = PRICING_MAP["aws_lb"].get(lb_type, 20.00)

                    elif resource_type == "aws_nat_gateway":
                         cost = PRICING_MAP["aws_nat_gateway"]["default"]

                    if cost > 0:
                        key = f"{resource_type}.{name}"
                        breakdown[key] = cost
                        total_cost += cost

        return {
            "total_monthly_cost": total_cost,
            "details": breakdown
        }
