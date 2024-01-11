import librosa
import noisereduce
import soundfile as sf

def remove_background_noise(input_audio_path, output_audio_path):
    # Загружаем аудиофайл
    audio, sr = librosa.load(input_audio_path, sr=None)

    # Применяем noisereduce к аудио
    reduced_noise = noisereduce.reduce_noise(audio, sr)

    # Сохраняем результат в новый аудиофайл
    sf.write(output_audio_path, reduced_noise, sr)

    print("Фоновый шум удален. Результат сохранен в", output_audio_path)
