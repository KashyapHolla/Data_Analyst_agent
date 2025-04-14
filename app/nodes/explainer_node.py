import pandas as pd
from app.config import get_prompt, LLM, log
from langchain.prompts import ChatPromptTemplate

def explainer_node(state: dict) -> dict:
    task_results = state.get("task_results", {})
    completed_tasks = state.get("completed_tasks", [])
    last_analysis = None

    for task_id in reversed(completed_tasks):
        result = task_results.get(task_id, {})
        if isinstance(result.get("df"), pd.DataFrame):
            last_analysis = result
            break

    if not last_analysis:
        return {**state, "summary": "No analysis available to summarize."}

    df = last_analysis["df"]
    preview = df.head(5).to_dict(orient="records")

    prompt_text = get_prompt("explainer")
    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = prompt | LLM
    result = chain.invoke({"preview": preview})
    summary = result.content.strip()

    return {**state, "summary": summary}
