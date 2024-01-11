from flask import Flask, render_template, redirect, url_for, request, send_file, send_from_directory
from text import ask_gpt
from image_gen import Text2ImageAPI
from audio import remove_background_noise
from video import remove_background
import os
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

AUDIO_FOLDER = 'static/audio/'
app.config['AUDIO_FOLDER'] = 'static/audio/'

VIDEO_FOLDER = 'static/video/'
app.config['VIDEO_FOLDER'] = 'static/video/'

messages_len = 30
messages = []

@app.route("/")
@app.route("/home")
def home():
    return render_template("index_new.html")

@app.route("/prompts")
def prompts():
    return render_template("prompts.html")

@app.route("/audio", methods=['GET', 'POST'])
def process_audio():
    if request.method == 'POST':
        # Получаем загруженный аудиофайл
        audio_file = request.files['audioFile']

        # Сохраняем загруженный файл
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], 'input_audio.wav')
        audio_file.save(audio_path)

        # Обрабатываем аудио для удаления фонового шума
        output_audio_path = os.path.join(app.config['AUDIO_FOLDER'], 'output_audio_cleaned.wav')
        remove_background_noise(audio_path, output_audio_path)

        # Предоставляем пути для отображения в HTML
        cleaned_audio = '/'.join(output_audio_path.split('/')[1:])
        download_link = f"/download/{'output_audio_cleaned.wav'}"

        return render_template("audio.html", cleaned_audio=cleaned_audio, download_link=download_link)

    return render_template("audio.html")

@app.route("/static/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

@app.route("/video", methods=['GET', 'POST'])
def process_video():
    if request.method == 'POST':
        # Получаем загруженный видеофайл
        video_file = request.files['videoFile']
        print("получен ", video_file)

        # Сохраняем загруженный файл
        video_path = 'static/videos/input_video.mp4'
        video_file.save(video_path)

        # Удаляем фон из видео
        output_video_path = 'static/videos/output_video_no_bg.mp4'
        remove_background(video_path, output_video_path)

        # Предоставляем пути для отображения в HTML
        input_video = '/'.join(video_path.split('/')[1:])
        output_video = '/'.join(output_video_path.split('/')[1:])
        download_link = f"/download/{'output_video_no_bg.mp4'}"

        return render_template("video.html", input_video=input_video, output_video=output_video, download_link=download_link)

    return render_template("video.html")

@app.route("/download_video/<path:filename>")
def download_video(filename):
    return send_file(f'static/videos/{filename}', as_attachment=True)

@app.route("/static/video/<path:filename>")
def serve_video(filename):
    return send_from_directory(app.config['VIDEO_FOLDER'], filename)

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

@app.route("/image", methods=['GET', 'POST'])
def generate_images():
    if request.method == 'POST':
        prompt = request.form.get('prompt')

        # Генерация изображений
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'B2C4685CA7669D34FB7A0081595FE330', 'C235FDD9A9E04C805E1DBE1CE49DB2AA')
        model_id = api.get_model()
        uuid = api.generate(prompt, model_id, images=3)
        images = api.check_generation(uuid)

        # Создаем папку для сохранения изображений
        image_folder = os.path.join(app.config['UPLOAD_FOLDER'], prompt.replace(" ", "_"))
        os.makedirs(image_folder, exist_ok=True)

        # Сохраняем изображения
        for i, image_base64 in enumerate(images):
            image_data = base64.b64decode(image_base64)
            image_path = os.path.join(image_folder, f"image_{i + 1}.jpg")
            with open(image_path, "wb") as file:
                file.write(image_data)

        # Список файлов для передачи на страницу
        image_files = [f"{prompt.replace(' ', '_')}/image_{i + 1}.jpg" for i in range(len(images))]

        return render_template("image.html", prompt=prompt, image_files=image_files)
    return render_template("image.html")

@app.route("/download_image/<path:filename>")
def download_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)