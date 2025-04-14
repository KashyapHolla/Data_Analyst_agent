from langchain.prompts import ChatPromptTemplate
from app.config import LLM, get_prompt, log
import json

# Load prompt from file
prompt_text = get_prompt("task_planner")
prompt = ChatPromptTemplate.from_template(prompt_text)

def task_planner_node(state: dict) -> dict:
    parsed_input = state.get("parsed_input")

    if not parsed_input:
        return {**state, "task_plan": [{"error": "Missing parsed_input"}]}

    chain = prompt | LLM
    result = chain.invoke({"input": parsed_input})

    try:
        plan = json.loads(result.content.strip())
    except json.JSONDecodeError:
        plan = [{"error": "Planning failed", "raw_output": result.content}]

    log(f"Generated task plan: {[t['id'] for t in plan if 'id' in t]}")
    
    return {**state, "task_plan": plan}
