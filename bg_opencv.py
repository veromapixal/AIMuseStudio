#удаление фона
#вариант с opencv
# Установка необходимых библиотек
# pip install Flask
# pip install opencv-python
# pip install numpy
# pip install Pillow

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Папка для загруженных изображений
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background(image_path):
    # Загрузка изображения с помощью OpenCV
    image = cv2.imread(image_path)
    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Применение алгоритма выделения объектов (например, алгоритм Canny)
    edges = cv2.Canny(gray, 50, 150)
    # Применение алгоритма поиска контуров
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Создание маски с белым фоном
    mask = np.ones_like(image) * 255
    # Заполнение обнаруженных контуров черным цветом на маске
    cv2.drawContours(mask, contours, -1, (0, 0, 0), thickness=cv2.FILLED)
    # Замена фона на белый цвет
    result = np.where(mask == 0, image, 255)
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Удаление фона и сохранение измененного изображения
        result_image = remove_background(filepath)
        result_filename = 'result_' + filename
        result_filepath = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_filepath, result_image)

        return render_template('result.html', original=filename, result=result_filename)

    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
