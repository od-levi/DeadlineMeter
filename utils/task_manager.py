# utils/task_manager.py

import uuid
from datetime import date

def add_task(session_state, task_name, deadline):
    today = date.today()
    days_left = (deadline - today).days

    if days_left > 7:
        status = "Chill"
    elif days_left >= 3:
        status = "Start Planning"
    elif days_left >= 0:
        status = "Panic"
    else:
        status = "Missed deadline"

    # Prevent duplicates
    existing_ids = [t["id"] for t in session_state.tasks]
    if not any(t["name"] == task_name and t["deadline"] == deadline for t in session_state.tasks):
        session_state.tasks.append({
            "id": str(uuid.uuid4()),
            "name": task_name,
            "deadline": deadline,
            "days_left": days_left,
            "status": status
        })

def delete_task(session_state, task_id):
    session_state.tasks = [t for t in session_state.tasks if t["id"] != task_id]

def mark_task_done(session_state, task, done_tasks_limit=5):
    if not any(dt["id"] == task["id"] for dt in session_state.done_tasks):
        session_state.done_tasks.append(task)
        # Remove from active tasks
        delete_task(session_state, task["id"])
        # Limit done tasks
        if len(session_state.done_tasks) > done_tasks_limit:
            session_state.done_tasks.pop(0)

def restore_task(session_state, task):
    # Remove from done_tasks
    session_state.done_tasks = [dt for dt in session_state.done_tasks if dt["id"] != task["id"]]
    # Add back to tasks
    session_state.tasks.append(task)