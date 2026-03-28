from google.adk.agents.llm_agent import Agent

# ---------------------------------------------------------
# 1. Define the Custom Tool
# ---------------------------------------------------------
def calculate_priority_score(has_deadline: bool, is_legal_or_financial: bool) -> str:
    """
    Calculates a standardized priority score for a task or message.
    
    Args:
        has_deadline: True if the text mentions a specific date or time to complete a task.
        is_legal_or_financial: True if the text mentions legal, compliance, billing, contracts, or financial consequences.
        
    Returns:
        A string indicating the official Priority Level.
    """
    if has_deadline and is_legal_or_financial:
        return "CRITICAL - Immediate Action Required"
    elif has_deadline:
        return "HIGH - Time Sensitive"
    elif is_legal_or_financial:
        return "MEDIUM - Important but not strictly timed"
    else:
        return "ROUTINE - Process when able"


# ---------------------------------------------------------
# 2. Define the Agent and give it access to the Tool
# ---------------------------------------------------------
root_agent = Agent(
    model='gemini-2.5-flash',
    name='clearmind_agent',
    description='An accessibility assistant that extracts summaries and uses tools to calculate priority.',
    # Give the agent access to our custom tool(s)
    tools=[calculate_priority_score],
    instruction=(
        "You are 'ClearMind', a cognitive load reducer and accessibility assistant. "
        "Your job is to read complex or bureaucratic text and simplify it. "
        "IMPORTANT RULES: "
        "1. You MUST use the `calculate_priority_score` tool to determine the URGENCY. Pass the correct boolean values based on the user's text. "
        "2. Never guess the urgency yourself; always use the tool's output. "
        "3. Format your final response exactly like this:\n\n"
        "**SUMMARY:**\n[1-2 sentences explaining what happened]\n\n"
        "**ACTION ITEMS:**\n[Bulleted list of things the user needs to do, or 'None required']\n\n"
        "**DEADLINES:**\n[Bulleted list of exact dates/times, or 'No deadlines mentioned']\n\n"
        "**URGENCY:**\n[The exact string returned by the calculate_priority_score tool]"
    )
)