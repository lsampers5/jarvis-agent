from agent import run_agent_turn
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

    messages = run_agent_turn(messages)

    print(f"Jarvis: {messages[-1]['content']}")
   

