import requests

print("Jarvis (via server) is online. Type 'quit' to exit.")
session_id = "luke-terminal"

while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "quit()", "q"):
        print("Jarvis: Goodbye!")
        break

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json = {"session_id": session_id, "message": user_input}
    )

    data = response.json()
    reply = data.get("reply") if data else "Sorry, I had trouble generating a response."
    print(f"Jarvis: {reply}")