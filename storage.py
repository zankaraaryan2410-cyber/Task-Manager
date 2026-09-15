import pandas as pd
import os

COLUMNS = ["task_id", "task_name", "priority", "status", "due_date"]
FILE_PATH = "data/tasks.csv"


def load_task():
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        print("Tasks loaded successfully.")
        return df
    else:
        print("No task file found. Starting with empty data.")
        return pd.DataFrame(columns=COLUMNS)


def save_task(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(FILE_PATH, index=False)
    print("Tasks saved successfully.")