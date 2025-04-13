import os
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage

# ===========
# BASE CONFIG
# ===========

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data Folders
DATA_PATH = PROJECT_ROOT / "data"

# Prompt Folders
PROMPT_PATH = PROJECT_ROOT / "app" / "prompts"

# File extensions supported
SUPPORTED_FILE_EXTENSIONS = [".csv", ".xls", ".xlsx"]

# Enable debug/verbose logs
DEBUG = True

# ===========
# LLM CONFIG
# ===========

# Ollama local model
LLM = ChatOllama(model="deepseek-r1:14b", temperature=0.2)

def get_prompt(name: str) -> str:
    """
    Load a prompt from the prompt folder by name.
    """

    file_path = PROMPT_PATH / f"{name}.txt"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt not found: {file_path}")
    
    with open(file_path, "r") as f:
        return f.read()
    
def log(message: str):
    """
    Conditional logger.
    """
    
    if DEBUG:
        print(f"[DEBUG] {message}")

# Simple test when run directly
if __name__ == "__main__":
    print("Testing LLM configuration...")
    try:
        user_prompt = input("Enter your prompt for the LLM: ")
        response = LLM.invoke([HumanMessage(content=user_prompt)])
        print(f"LLM Response: {response.content}")
        print("LLM configuration test successful!")
    except Exception as e:
        print(f"Error testing LLM configuration: {e}")


