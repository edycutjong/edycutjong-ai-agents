import pandas as pd
import numpy as np
from datetime import timedelta

class CostAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_total_cost(self) -> float:
        return self.df['Cost'].sum()

    def calculate_cost_by_service(self) -> pd.DataFrame:
        return self.df.groupby('Service')['Cost'].sum().sort_values(ascending=False).reset_index()

    def calculate_daily_trend(self) -> pd.DataFrame:
        if 'Date' not in self.df.columns:
            return pd.DataFrame()
        # Ensure Date is datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        return self.df.groupby(self.df['Date'].dt.date)['Cost'].sum().reset_index()

    def identify_potential_waste(self) -> pd.DataFrame:
        """
        Identifies potential waste based on heuristics.
        Returns a DataFrame of flagged resources.
        """
        waste_flags = []

        # 1. Unattached Resources (e.g., Elastic IPs with Cost > 0 but low usage/network in)
        # Heuristic: 'ElasticIP' in Service and Cost > 0
        # (This is a simplified example)
        if 'Service' in self.df.columns:
            eip_waste = self.df[
                (self.df['Service'].str.contains('ElasticIP', case=False, na=False)) &
                (self.df['Cost'] > 0)
            ].copy()
            if not eip_waste.empty:
                eip_waste['Reason'] = 'Potential Unattached IP'
                waste_flags.append(eip_waste)

        # 2. Old Snapshots (if 'Snapshot' in Service and Date < X days ago)
        # Using a dummy check for now
        if 'Service' in self.df.columns and 'Date' in self.df.columns:
            snapshot_waste = self.df[
                (self.df['Service'].str.contains('Snapshot', case=False, na=False)) &
                (self.df['Date'] < (pd.Timestamp.now() - timedelta(days=90)))
            ].copy()
            if not snapshot_waste.empty:
                snapshot_waste['Reason'] = 'Old Snapshot (>90 days)'
                waste_flags.append(snapshot_waste)

        # 3. Underutilized Instances (Mock check if 'CPUUtilization' column exists)
        if 'CPUUtilization' in self.df.columns:
            low_cpu = self.df[
                (self.df['CPUUtilization'] < 5.0) &
                (self.df['Service'].str.contains('Instance|EC2|Compute', case=False, na=False))
            ].copy()
            if not low_cpu.empty:
                low_cpu['Reason'] = 'Low CPU Utilization (<5%)'
                waste_flags.append(low_cpu)

        if waste_flags:
            return pd.concat(waste_flags)
        else:
            return pd.DataFrame(columns=['Service', 'ResourceID', 'Cost', 'Reason'])

    def detect_anomalies(self, threshold_std=2.0) -> pd.DataFrame:
        """
        Detects cost spikes using Z-score on daily costs.
        """
        daily = self.calculate_daily_trend()
        if daily.empty or len(daily) < 3:
            return pd.DataFrame()

        mean_cost = daily['Cost'].mean()
        std_cost = daily['Cost'].std()

        if std_cost == 0:
            return pd.DataFrame()

        daily['Z-Score'] = (daily['Cost'] - mean_cost) / std_cost
        anomalies = daily[daily['Z-Score'] > threshold_std].copy()
        return anomalies
