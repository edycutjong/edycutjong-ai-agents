import datetime
import pandas as pd

def get_current_time():
    # Deprecated
    return datetime.datetime.utcnow()

def add_data():
    df = pd.DataFrame({'a': [1, 2]})
    new_row = pd.DataFrame({'a': [3]})
    # Deprecated
    return df.append(new_row)
