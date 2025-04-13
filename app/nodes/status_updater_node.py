def state_updater_node(state: dict) -> dict:
    """
    A passthrough node to cleanly update and return the state.
    Useful between tool execution and looping back to dispatcher.
    """
    return state
