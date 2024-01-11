import g4f

def ask_gpt(messages: list) -> str:
    print(messages)
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=messages
        )

        print(response)
        # Получение текста ответа
        return response
    except Exception as e:
        print(f"Error during ask_gpt: {e}")
        return "Error during ask_gpt"

def main():
    messages_len = 30
    messages = []

    while True:

        user_input = input("You: ")

        if len(messages) > messages_len:
            messages = messages[-messages_len:]
        messages.append({"role": "user", "content": user_input})

        gpt_response = ask_gpt(messages=messages)
        print(f"GPT: {gpt_response}")
        messages.append({"role": "assistant", "content": gpt_response})

if __name__ == "__main__":
    main()
