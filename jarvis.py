import ollama
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


print("Jarvis is online. Type 'quit' to exit.")

messages = [
    {"role": "system", "content": "You are Jarvis, a helpful personal assistant. Be concise and friendly."}
]

while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "quit()", "q"):
        print("Jarvis: Goodbye!")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = ollama.chat(model="qwen2.5:3b", messages=messages, tools=[calculate_tool, internet_search_tool])
    # Did the model ask for a tool?
    if response.message.tool_calls:
        # Yes - add models request to the conversation
        messages.append(response.message)

        # Run the tools the models asked for
        for tool_call in response.message.tool_calls:
            if tool_call.function.name == "internet_search":
                search_query = tool_call.function.arguments["search_query"]
                result = internet_search(search_query)
            elif tool_call.function.name == "calculate":
                expression = tool_call.function.arguments["expression"]
                result = calculate(expression)

            messages.append({
                "role": "tool",
                "content": str(result)
            })
        # Ask the model again, now that is has the answer
        response = ollama.chat(
            model="llama3.2",
              messages=messages,
              tools=[calculate_tool, internet_search_tool],
              options = {"temperature": 0.2}
              )
    

    # Print the models final reply
    jarvis_reply = response.message.content
    messages.append({"role": "assistant", "content": jarvis_reply})
    
    print(f"Jarvis: {jarvis_reply}")

