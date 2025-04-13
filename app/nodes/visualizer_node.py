import pandas as pd
import matplotlib.pyplot as plt
import uuid
from app.config import OUTPUT_PATH, log

def visualizer_node(state: dict) -> dict:
    """
    Visualizes data using matplotlib.
    """

    current_tasks = state.get("current_tasks", [])
    task_results = state.get("task_results", {})
    completed_tasks = state.get("completed_tasks", [])

    for task in current_tasks:
        if task["type"] != "plot":
            continue

        task_id = task["id"]
        chart_type = task.get("chart", "bar")
        depends_on = task["depends_on"]

        data = task_results.get(depends_on, {}).get("df")
        if data is None or not isinstance(data, pd.DataFrame):
            task_results[task_id] = {"error": "No valid data for visualization"}
            completed_tasks.append(task_id)
            continue
        
        try:
            fig, ax = plt.subplots()
            if chart_type == "line":
                data.plot(ax=ax)
            elif chart_type == "bar":
                data.plot(kind="bar", ax=ax)
            elif chart_type == "pie":
                data.set_index(data.columns[0]).plot(kind="pie", y=data.columns[1], ax=ax, legend=False)
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")

            fig_id = f"{task_id}_{uuid.uuid4().hex[:8]}.png"
            chart_path = OUTPUT_PATH / fig_id
            plt.title(task.get("title", "Generated Chart"))
            plt.tight_layout()
            plt.savefig(chart_path)
            plt.close()

            task_results[task_id] = {
                "chart_path": str(chart_path),
                "description": f"{chart_type.title()} chart saved to {chart_path.name}"
            }

        except Exception as e:
            task_results[task_id] = {"error": str(e)}

        completed_tasks.append(task_id)

    return {
        **state,
        "task_results": task_results,
        "completed_tasks": completed_tasks
    }