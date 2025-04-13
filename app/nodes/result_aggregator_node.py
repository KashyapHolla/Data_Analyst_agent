import pandas as pd

def result_aggregator_node(state: dict) -> dict:
    """
    Collects multiple analysis outputs and combines them if needed.
    For example: join data from two analyses into one dataframe.
    """
    task_results = state.get("task_results", {})
    completed_tasks = state.get("completed_tasks", [])

    dfs = [
        task_results[tid]["df"]
        for tid in completed_tasks
        if "df" in task_results.get(tid, {}) and isinstance(task_results[tid]["df"], pd.DataFrame)
    ]

    if len(dfs) > 1:
        try:
            result = pd.concat(dfs, axis=0)
            task_results["aggregated"] = {
                "df": result,
                "preview": result.head().to_dict(orient="records")
            }
            completed_tasks.append("aggregated")
        except Exception as e:
            task_results["aggregated"] = {"error": str(e)}

    return {
        **state,
        "task_results": task_results,
        "completed_tasks": completed_tasks
    }
