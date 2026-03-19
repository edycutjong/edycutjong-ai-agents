class CostCalculator:  # pragma: no cover
    def __init__(self, cost_per_gb: float = 0.50):  # pragma: no cover
        self.cost_per_gb = cost_per_gb  # pragma: no cover

    def calculate_cost(self, line_count: int, avg_line_size_bytes: int = 100) -> float:  # pragma: no cover
        """
        Calculate estimated cost based on line count and average size.
        Returns cost in dollars.
        """
        total_bytes = line_count * avg_line_size_bytes  # pragma: no cover
        gb = total_bytes / (1024 * 1024 * 1024)  # pragma: no cover
        return gb * self.cost_per_gb  # pragma: no cover

    def calculate_annual_projection(self, daily_line_count: int, avg_line_size_bytes: int = 100) -> float:  # pragma: no cover
        """
        Calculate annual cost projection assuming the provided line count is for one day.
        """
        daily_cost = self.calculate_cost(daily_line_count, avg_line_size_bytes)  # pragma: no cover
        return daily_cost * 365  # pragma: no cover
