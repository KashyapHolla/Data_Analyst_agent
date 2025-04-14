from langchain.prompts import ChatPromptTemplate
from app.config import LLM, get_prompt
import json

# Load prompt from file
PARSER_INPUT = get_prompt("input_parser")
prompt = ChatPromptTemplate.from_template(PARSER_INPUT)

def input_parser_node(state: dict) -> dict:
    """
    Parses the user's request into structured fields.
    """
    # Get the user's input
    user_input = state.get("input")
    
    # Define the chain
    chain = prompt | LLM
    result = chain.invoke({"input": user_input})

    try:
        parsed = json.loads(result.content.strip())
    except Exception as e:
        parsed = {
            "error": "parsing failed",
            "raw_output":str(e)
        }
    
    return {
        **state,
        "parsed_input": parsed
    }

