import pandas as pd
import traceback
from app.config import LLM, get_prompt, log

# Load the code-gen prompt
CODE_GEN_PROMPT = get_prompt("code_generator")

def analysis_executor_node(state: dict) -> dict:
    """
    Uses LLM to generate and run pandas code to perform analysis.
    """
    current_tasks = state.get("current_tasks", [])
    task_results = state.get("task_results", {})
    completed_tasks = state.get("completed_tasks", [])

    for task in current_tasks:
        task_id = task["id"]
        task_type = task.get("type", "")

        if task_type != "analyze" or task_id in completed_tasks:
            continue
        
        # Get the source DataFrame on which the analysis depends
        depends_on = task.get("depends_on")
        source_df = task_results.get(depends_on, {}).get("df", None)

        if source_df is None:
            task_results[task_id] = {"error": "Missing input DataFrame"}
            completed_tasks.append(task_id)
            continue


        try:
            # Generate code from the LLM
            user_query = task.get("query")
            context_df_preview = source_df.head(5).to_dict(orient="records")
            column_names = source_df.columns.tolist()

            # Defining LLM chain
            chain = CODE_GEN_PROMPT| LLM 
            result = chain.invoke({
                "query": user_query,
                "columns": column_names,
                "preview": context_df_preview
            })

            # Execute the generated code
            generated_code = result.context.strip()
            log(f"Generated code:\n {generated_code}")

            # Execute the code
            local_vars = {"df": source_df.copy(), "pd": pd}
            exec(generated_code, {}, local_vars)
            # Get the result
            result = local_vars.get("result", None)

            if not isinstance(result, pd.DataFrame):
                raise ValueError("Result must be a pandas DataFrame.")
            
            # Store the result
            task_results[task_id] = {
                "df": result,
                "preview": result.head().to_dict(orient="records"),
                "code": generated_code
            }

        except Exception as e:
            task_results[task_id] = {
                "error": str(e),
                "traceback": traceback.format_exc(),
                "code": generated_code if 'generated_code' in locals() else None,
            }
            log(f"Error executing analysis for task {task_id}: {e}")
        
        completed_tasks.append(task_id)
        
    return {
        **state,
        "task_results": task_results,
        "completed_tasks": completed_tasks
    }