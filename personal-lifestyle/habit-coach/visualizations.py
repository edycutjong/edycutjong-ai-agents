import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta
try:
    from .storage import get_logs, get_habits
except ImportError:
    from storage import get_logs, get_habits

def plot_habit_progress(habit_id: str, days: int = 30):
    logs = get_logs(habit_id)
    habit_name = next((h.name for h in get_habits() if h.id == habit_id), "Unknown Habit")

    # Create a date range for the last N days
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    date_range = [start_date + timedelta(days=i) for i in range(days)]

    # Map logs to status (1 for completed, 0 for otherwise)
    status_map = {l.date: 1 if l.status == 'completed' else 0 for l in logs}
    data = [{'date': d, 'status': status_map.get(d, 0)} for d in date_range]

    df = pd.DataFrame(data)

    fig = px.bar(df, x='date', y='status', title=f"Progress: {habit_name} (Last {days} Days)")
    fig.update_yaxes(tickvals=[0, 1], ticktext=['Missed', 'Completed'])
    return fig

def plot_heatmap(habit_id: str):
    # Github-style contribution graph: X=Week, Y=Weekday
    logs = get_logs(habit_id)
    habit_name = next((h.name for h in get_habits() if h.id == habit_id), "Unknown Habit")

    if not logs:
        return go.Figure().update_layout(title=f"No data for {habit_name}")

    # Generate data for the last year (or since creation)
    # Let's do last 52 weeks
    end_date = date.today()
    start_date = end_date - timedelta(weeks=52)
    # Align start_date to Monday
    start_date = start_date - timedelta(days=start_date.weekday())

    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    completed_dates = {l.date for l in logs if l.status == 'completed'}

    data = []
    for d in date_range:
        # ISO week number and weekday
        year, week, weekday = d.isocalendar()
        # weekday: 1=Mon, 7=Sun. Map to 0-6
        day_idx = weekday - 1

        # We want X to be date or week.
        # Easier to just pass date and let Plotly handle it if we use heatmap
        # But for GitHub style, we need discrete coordinates

        data.append({
            'date': d,
            'week': f"{year}-W{week:02d}", # Group key
            'weekday': day_idx, # 0=Mon, 6=Sun
            'status': 1 if d in completed_dates else 0,
            'day_name': d.strftime("%a")
        })

    df = pd.DataFrame(data)

    # Pivot to matrix form for heatmap
    # We need a matrix where rows=Weekday (Mon-Sun), cols=Week
    # But doing this manually is tedious with weeks spanning years.

    # Let's try a simpler approach: Scatter plot with squares
    # Y = Weekday, X = Week Start Date

    df['week_start'] = df['date'].apply(lambda x: x - timedelta(days=x.weekday()))

    fig = go.Figure(data=go.Heatmap(
        z=df['status'],
        x=df['week_start'],
        y=df['day_name'],
        colorscale=[[0, '#ebedf0'], [1, '#40c463']], # GitHub colorsish
        showscale=False,
        ygap=2,
        xgap=2
    ))

    fig.update_layout(
        title=f"Activity Heatmap: {habit_name}",
        yaxis=dict(
            categoryorder='array',
            categoryarray=['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon']
        ),
        height=250
    )
    return fig

def plot_completion_rate_trend(habit_id: str):
    # Monthly completion rate
    logs = get_logs(habit_id)
    habit_name = next((h.name for h in get_habits() if h.id == habit_id), "Unknown Habit")

    if not logs:
        return go.Figure()

    df = pd.DataFrame([{'date': l.date, 'status': 1 if l.status == 'completed' else 0} for l in logs])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    monthly = df.resample('M')['status'].mean() * 100

    fig = px.line(monthly, title=f"Monthly Completion Rate: {habit_name}")
    fig.update_yaxes(title="Completion %")
    return fig
