from ddgs import DDGS

# Calculate Function
# Function
def calculate(expression: str):
    print(f"\n[DEBUG] Calculate tool called with the experession: '{expression}'\n")
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: could not find expression '{expression}': {e}"

# Tool Description
calculate_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Only evaluates math expressions and returns the result. Use this strictly for any arithmetic.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate, e.g. '4*4' or '100/10'"
                }
            },
            "required": ["expression"]
        }
    }
}
def internet_search(search_query: str):
    results = DDGS().text(search_query, max_results=3)
    print(f"\n[DEBUG] Search Query: {search_query}")
    print(f"\n[DEBUG] Raw results: {results}\n")
    return str(results)
# Search Tool Description - Need Claude to make sure that it is okay - Add function above.
internet_search_tool = {
    "type": "function",
    "function": {
        "name": "internet_search",
        "description": "Searches the internet and looks for up to date relevant information and returns a collective summary of what it finds. Use this when looking up about recent events. Do NOT use for greetings, small talk, or general conversation (e.g. 'How are you', 'hello', 'what can you do') - Respond to those directly without searching.",
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "The topic of search, e.g. 'Most recent World Cup game' or 'Weather in Newark New Jersey right now'"
                }
            },
            "required": ["search_query"]
        }
    }
}
