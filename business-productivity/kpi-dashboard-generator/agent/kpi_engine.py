import pandas as pd

class KPIDefinition:
    def __init__(self, name, column, aggregation, target, format_str="{:.2f}", logic='higher_is_better'):
        self.name = name
        self.column = column
        self.aggregation = aggregation # 'sum', 'avg', 'count', 'min', 'max'
        self.target = float(target)
        self.format_str = format_str
        self.logic = logic # 'higher_is_better' or 'lower_is_better'

class KPIEngine:
    @staticmethod
    def calculate_metric(df, kpi_def):
        """Calculates the metric value based on the KPI definition."""
        # Special case for counting rows (record count)
        if kpi_def.aggregation == 'count' and (kpi_def.column == 'Rows' or kpi_def.column is None):
            return len(df)

        if kpi_def.column not in df.columns:
            return None

        series = df[kpi_def.column]

        # Ensure numeric for calculations (except count, though count usually implies presence)
        if kpi_def.aggregation != 'count':
             try:
                series = pd.to_numeric(series, errors='coerce')
             except:
                 return None

        if kpi_def.aggregation == 'sum':
            return series.sum()
        elif kpi_def.aggregation == 'avg' or kpi_def.aggregation == 'mean':
            return series.mean()
        elif kpi_def.aggregation == 'count':
            return series.count()
        elif kpi_def.aggregation == 'min':
            return series.min()
        elif kpi_def.aggregation == 'max':
            return series.max()
        else:
            raise ValueError(f"Unknown aggregation: {kpi_def.aggregation}")

    @staticmethod
    def evaluate_status(value, target, logic='higher_is_better'):
        """Evaluates if the metric is good (success), warning, or bad (danger)."""
        if value is None:
            return "unknown"

        # Simple threshold logic: within 10% of target is warning
        if logic == 'higher_is_better':
            if value >= target:
                return "success"
            elif value >= target * 0.9:
                return "warning"
            else:
                return "danger"
        else: # lower_is_better
            if value <= target:
                return "success"
            elif value <= target * 1.1:
                return "warning"
            else:
                return "danger"
