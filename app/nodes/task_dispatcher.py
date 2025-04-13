from app.config import log

def get_ready_tasks(task_plan, completed_task_ids):
    ready = []
    for task in task_plan:
        task_id = task["id"]
        depends_on = task.get("depends_on")

        if task_id in completed_task_ids:
            continue

        # Handle single or multiple dependencies
        if depends_on is None:
            ready.append(task)
        elif isinstance(depends_on, str):
            if depends_on in completed_task_ids:
                ready.append(task)
        elif isinstance(depends_on, list):
            if all(dep in completed_task_ids for dep in depends_on):
                ready.append(task)
    return ready

def task_dispatcher_node(state: dict) -> dict:
    task_plan = state.get("task_plan", [])
    completed_tasks = state.get("completed_tasks", [])
    task_results = state.get("task_results", {})

    ready_tasks = get_ready_tasks(task_plan, completed_tasks)

    log(f"Completed Tasks: {completed_tasks}")
    log(f"Ready Tasks: {[task['id'] for task in ready_tasks]}")

    if not ready_tasks:
        return {**state, "current_tasks": [], "status": "done"}

    return {
        **state,
        "current_tasks": ready_tasks,
        "status": "in_progress"
    }
