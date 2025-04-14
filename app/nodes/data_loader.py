import pandas as pd
from pathlib import Path
from app.config import DATA_PATH, SUPPORTED_FILE_EXTENSIONS, log

#=============
# Sample task input dispatcher might receive
# {
#     "id": "load_data",
#     "type": "load_csv",
#     "file": "sales.csv",
#     "deppends_on": null
# }
#=============

def data_loader_node(state: dict) -> dict:
    """
    Loads dataset file specified in the current task.
    Stores it in the task_results and marks the task as completed.
    """

    current_task = state.get("current_task", [])
    task_results = state.get("task_results", {})
    completed_tasks = state.get("completed_tasks", [])

    # Loop through current tasks (Might also have multiple tasks in parallel)
    for task in current_task:
        if task["type"] not in ["load_csv", "load_data"]:
            continue
        
        # Getting the file name and task id
        file_name = task.get("file", "")
        task_id = task[id]

        # Getting the file path
        file_path = Path(DATA_PATH) / file_name
        log(f"Loading file: {file_path}")

        if not file_path.exists():
            task_results[task_id] = {"error": f"File not found: {file_name}"}
            completed_tasks.append(task_id)
            continue

        try:
            if file_path.suffix == ".csv":
                df = pd.read_csv(file_path)
            elif file_path.suffix == ".xls" or file_path.suffix == ".xlsx":
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file extension: {file_path.suffix}")
                
            # Saving results
            task_results[task_id] = {
                "df": df,
                "columns": df.columns.tolist(),
            }

            completed_tasks.append(task_id)
            log(f"Loaded file: {file_name} with {df.shape[0]} rows and {df.shape[1]} columns")

        except Exception as e:
            task_results[task_id] = {"error": str(e)}
            completed_tasks.append(task_id)
            log(f"Error loading file {file_name}: {e}")


    return {
        **state,
        "task_results": task_results,
        "completed_tasks": completed_tasks
    }
        