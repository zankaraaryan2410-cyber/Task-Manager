import pandas as pd
from storage import COLUMNS


def _next_id(df):

    return int(df["task_id"].max()) + 1 if not df.empty else 1


def _id_exists(df, task_id):

    return task_id in df["task_id"].values


def add_task(df, name, priority, due_date):

    name = name.strip()
    priority = priority.strip().capitalize()
    due_date = due_date.strip()

    if priority not in ["High", "Medium", "Low"]:
        return df

    new_row = pd.DataFrame([{
        "task_id": _next_id(df),
        "task_name": name,
        "priority": priority,
        "status": "Pending",
        "due_date": due_date
    }])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    return df


def sort_by_priority(df):

    order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    sorted_df = df.copy()

    sorted_df["_order"] = sorted_df["priority"].map(order)

    sorted_df = sorted_df.sort_values("_order")

    sorted_df = sorted_df.drop(columns=["_order"])

    return sorted_df


def update_task(df, task_id, name=None, priority=None, due_date=None):

    if not _id_exists(df, task_id):
        return df

    if name is not None:
        df.loc[
            df["task_id"] == task_id,
            "task_name"
        ] = name

    if priority is not None:

        priority = priority.capitalize()

        if priority not in ["High", "Medium", "Low"]:
            return df

        df.loc[
            df["task_id"] == task_id,
            "priority"
        ] = priority

    if due_date is not None:
        df.loc[
            df["task_id"] == task_id,
            "due_date"
        ] = due_date

    return df


def mark_done(df, task_id):

    if not _id_exists(df, task_id):
        return df

    df.loc[
        df["task_id"] == task_id,
        "status"
    ] = "Done"

    return df


def delete_task(df, task_id):

    if not _id_exists(df, task_id):
        return df

    df = df[
        df["task_id"] != task_id
    ].reset_index(drop=True)

    return df


def remove_done(df):

    df = df[
        df["status"] != "Done"
    ].reset_index(drop=True)

    return df


def search_task(df, keyword):

    keyword = keyword.strip().lower()

    result = df[
        df["task_name"]
        .str.lower()
        .str.contains(keyword, na=False)
    ]

    return result