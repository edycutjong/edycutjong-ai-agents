import pandas as pd

class Recommender:
    def __init__(self, waste_df: pd.DataFrame):
        self.waste_df = waste_df

    def suggest_right_sizing(self) -> pd.DataFrame:
        """
        Suggests right-sizing based on low utilization.
        Assuming 'InstanceType' column exists or can be inferred.
        """
        suggestions = []

        # Simplified Mock Mapping
        instance_map = {
            'm5.2xlarge': 'm5.xlarge',
            'm5.xlarge': 'm5.large',
            't3.large': 't3.medium',
            'Standard_D4s_v3': 'Standard_D2s_v3' # Azure
        }

        if 'InstanceType' in self.waste_df.columns:
            for idx, row in self.waste_df.iterrows():
                current_type = row.get('InstanceType')
                reason = row.get('Reason')

                if 'Low CPU' in str(reason) and current_type in instance_map:
                    suggestions.append({
                        'ResourceID': row.get('ResourceID'),
                        'CurrentType': current_type,
                        'SuggestedType': instance_map[current_type],
                        'EstimatedSavings': row.get('Cost') * 0.4 # Assume 40% saving
                    })

        return pd.DataFrame(suggestions)

    def calculate_total_potential_savings(self) -> float:
        """
        Calculates total potential savings from flagged waste.
        """
        if self.waste_df.empty:
            return 0.0

        # If specific estimated savings exist, sum them up
        # Otherwise, assume 100% savings for waste (e.g., deleted resources)
        # For simplicity, let's say "Old Snapshots" = 100% waste cost
        # "Unattached IP" = 100% waste cost
        # "Low Utilization" = 40% waste cost (downsizing)

        total_savings = 0.0

        for idx, row in self.waste_df.iterrows():
            reason = str(row.get('Reason'))
            cost = row.get('Cost', 0.0)

            if 'Low CPU' in reason:
                total_savings += cost * 0.4
            else:
                total_savings += cost # Assume full removal

        return total_savings
