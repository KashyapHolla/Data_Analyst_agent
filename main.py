from app.graphs.analytics_flow import build_graph

# Define your user input query
user_input = "Compare subway ridership for the last 3 months with the same period last year."

# Build the graph
graph = build_graph()

# Run the agent
final_state = graph.invoke({"input": user_input})

# Print final output
print("\n--- SUMMARY ---")
print(final_state.get("summary"))

print("\n--- CHART PATH ---")
chart_info = final_state.get("task_results", {}).get("visualize", {})
print(chart_info.get("chart_path"))

print("\n--- CODE USED (if any) ---")
for task_id, result in final_state.get("task_results", {}).items():
    if "code" in result:
        print(f"\n[Code from task: {task_id}]\n")
        print(result["code"])
