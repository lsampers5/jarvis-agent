import ollama
from tools import calculate, internet_search, calculate_tool, internet_search_tool

TOOLS = [calculate_tool, internet_search_tool]
MODEL = "qwen2.5:3b"

def run_agent_turn(messages: list) -> list:
    response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS, options={"temperature": 0.2})
    print(f"\n[DEBUG] First response - content: {response.message.content}, tool_calls: {response.message.tool_calls}")

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

            messages.append({"role": "tool","content": str(result)})
        # Ask the model again, now that is has the answer
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        print(f"\n[DEBUG] Second response - content: {response.message.content}, tool_calls: {response.message.tool_calls}\n")
    

    # Print the models final reply
    jarvis_reply = response.message.content
    messages.append({"role": "assistant", "content": jarvis_reply})
    
    return messages