from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable

from app.nodes.input_parser import input_parser_node
from app.nodes.task_planner import task_planner_node
from app.nodes.task_dispatcher import task_dispatcher_node
from app.nodes.data_loader import data_loader_node
from app.nodes.analysis_executor import analysis_executor_node
from app.nodes.visualizer_node import visualizer_node
from app.nodes.explainer_node import explainer_node
from app.nodes.state_updater_node import state_updater_node

def build_graph() -> Runnable:

    # Create a new LangGraph
    builder = StateGraph()

    # Register all nodes
    builder.add_node("input_parser", input_parser_node)
    builder.add_node("task_planner", task_planner_node)
    builder.add_node("task_dispatcher", task_dispatcher_node)

    builder.add_node("data_loader", data_loader_node)
    builder.add_node("analysis_executor", analysis_executor_node)
    builder.add_node("visualizer", visualizer_node)

    builder.add_node("state_updater", state_updater_node)
    builder.add_node("explainer", explainer_node) 

    # #Entry point
    builder.set_entry_point("input_parser")

    # Core pipeline
    builder.add_edge("input_parser", "task_planner")
    builder.add_edge("task_planner", "task_dispatcher")

    # Routing logic — all tool nodes go to state_updater
    builder.add_edge("data_loader", "state_updater")
    builder.add_edge("analysis_executor", "state_updater")
    builder.add_edge("visualizer", "state_updater")

    # After updater → back to dispatcher
    builder.add_edge("state_updater", "task_dispatcher")

    # When done → explainer → END
    builder.add_edge("explainer", END)

    # Add conditional logic at dispatcher
    def route_from_dispatcher(state: dict) -> str:
        status = state.get("status")
        current_tasks = state.get("current_tasks", [])

        if status == "done":
            return "explainer"

        if not current_tasks:
            return "task_dispatcher"

        task_type = current_tasks[0].get("type")
        routing_map = {
            "load_csv": "data_loader",
            "load_data": "data_loader",
            "analyze": "analysis_executor",
            "plot": "visualizer"
        }

        return routing_map.get(task_type, "state_updater")

    builder.add_conditional_edges("task_dispatcher", route_from_dispatcher)

    return builder.compile()
