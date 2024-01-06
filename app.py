from flask import Flask, render_template, redirect, url_for, request
from text import ask_gpt
app = Flask(__name__)

# Переменные для работы с OpenAI GPT
messages_len = 30
messages = []

#flask routing
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
@app.route("/clear")
def clear():
    global messages
    messages = []
    return redirect(url_for('chat'))
@app.route("/text", methods=['GET', 'POST'])
def chat():
    user_input = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        messages.append({"role": "user", "content": user_input})

        gpt_response = ask_gpt(messages=messages)
        messages.append({"role": "assistant", "content": gpt_response})

    return render_template("text.html", messages=messages, user_input=user_input)
#обработать ошибку Error during ask_gpt: RetryProvider failed:
#GptGo: ClientResponseError: 403, message='Forbidden', url=URL('https://gptgo.ai/get_token.php')
#ChatBase: ClientResponseError: 502, message='Bad Gateway', url=URL('https://www.chatbase.co/api/fe/chat')
#Chatgpt4Online: ClientResponseError: 403, message='Forbidden', url=URL('https://chatgpt4online.org/')
#You: RequestsError: Failed to perform, ErrCode: 77, Reason: 'error setting certificate verify locations:  CAfile: C:\Users\Компьютер\PycharmProjects\AIMuseStudio\venv\Lib\site-packages\curl_cffi\cacert.pem CApath: none'. This may be a libcurl error, See https://curl.se/libcurl/c/libcurl-errors.html first for more details.
#GptForLove: ProgramError: TypeError: Предполагается наличие объекта
#в html можно заменить message["content"] для исправления ошибки с ненужным выводом какой-то инфы от библы
#но тогда возникает ошибка, что он все выведенные ранее сообщения будет изменять на последний введенный текст

@app.route("/html")
def html():
    return render_template("new.html")

@app.route("/<name>")
def user(name):
    return f"Hello, {name}! How can I help you?"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)