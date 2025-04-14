# main.py

from app.graphs.agent_graph import build_agent_graph
from pathlib import Path

# Step 1: Define your user input and dataset
input_text = "Compare subway ridership for the last 3 months with the same period last year and summarize the trend."
dataset_path = Path("data/full_year_subway_ridership.csv")

# Step 2: Build the graph
graph = build_agent_graph()

# Step 3: Run the graph
final_state = graph.invoke({
    "input": input_text,
    "dataset_path": dataset_path
})

# Step 4: Output the results
print("\n✅ FINAL SUMMARY:")
print(final_state.get("final_summary", "[No summary generated]"))

print("\n📋 SUBTASK OUTPUTS:")
for idx, task in enumerate(final_state.get("subtask_outputs", [])):
    print(f"\n--- Subtask {idx + 1}: {task.get('subtask')}")
    if "preview" in task:
        print("Result Preview:", task["preview"])
    if "error" in task:
        print("Error:", task["error"])
