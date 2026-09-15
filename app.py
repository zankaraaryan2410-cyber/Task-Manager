from flask import Flask, render_template, request, redirect

from storage import load_task, save_task

from Operations import (
    add_task,
    sort_by_priority,
    update_task,
    mark_done,
    remove_done,
    delete_task,
    search_task
)


app = Flask(__name__)


def build_context(df, display_df, active_filter="all", sort_by=None):
    """Shared stats + template context used by every page that renders index.html."""

    total_tasks = len(df)
    pending_tasks = len(df[df["status"] == "Pending"])
    completed_tasks = len(df[df["status"] == "Done"])

    return dict(
        tasks=display_df.to_dict("records"),
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        active_filter=active_filter,
        sort_by=sort_by
    )


# ---------------- HOME ----------------

@app.route("/")
def home():

    df = load_task()

    active_filter = request.args.get("filter", "all")
    sort_by = request.args.get("sort")

    display_df = df

    if sort_by == "priority":
        display_df = sort_by_priority(display_df)

    if active_filter == "pending":
        display_df = display_df[display_df["status"] == "Pending"]
    elif active_filter == "completed":
        display_df = display_df[display_df["status"] == "Done"]

    context = build_context(df, display_df, active_filter, sort_by)

    return render_template("index.html", **context)


# ---------------- ADD TASK ----------------

@app.route("/add-task", methods=["GET", "POST"])
def add_task_route():
    if request.method == "GET":
        return render_template("add-task.html")

    if request.method == "POST":
        df = load_task()

        name = request.form["task_name"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]

        df = add_task(df, name, priority, due_date)
        save_task(df)

        return redirect("/")


# ---------------- EDIT TASK ----------------

@app.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task_route(task_id):

    df = load_task()

    if request.method == "POST":

        name = request.form["task_name"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]

        df = update_task(
            df,
            task_id,
            name=name,
            priority=priority,
            due_date=due_date
        )

        save_task(df)

        return redirect("/")

    task_row = df[df["task_id"] == task_id]

    if task_row.empty:
        return redirect("/")

    task = task_row.to_dict("records")[0]

    return render_template("edit-task.html", task=task)


# ---------------- MARK DONE ----------------

@app.route("/mark-done/<int:task_id>")
def mark_done_route(task_id):

    df = load_task()

    df = mark_done(
        df,
        task_id
    )

    save_task(df)

    return redirect("/")


# ---------------- DELETE SINGLE TASK ----------------

@app.route("/delete-task/<int:task_id>")
def delete_task_route(task_id):

    df = load_task()

    df = delete_task(
        df,
        task_id
    )

    save_task(df)

    return redirect("/")


# ---------------- REMOVE COMPLETED (bulk) ----------------

@app.route("/remove-done")
def remove_done_route():

    df = load_task()

    df = remove_done(df)

    save_task(df)

    return redirect("/")


# ---------------- SEARCH ----------------

@app.route("/search")
def search():

    keyword = request.args.get("keyword", "")

    df = load_task()

    result = search_task(df, keyword)

    context = build_context(df, result, active_filter="all", sort_by=None)

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=True)