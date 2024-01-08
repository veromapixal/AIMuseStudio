import librosa
import noisereduce
import soundfile as sf

def remove_background_noise(input_audio_path, output_audio_path):
    # Загрузите аудиофайл
    audio, sr = librosa.load(input_audio_path, sr=None)

    # Примените noisereduce к аудио
    reduced_noise = noisereduce.reduce_noise(audio, sr)

    # Сохраните результат в новый аудиофайл
    sf.write(output_audio_path, reduced_noise, sr)

    print("Фоновый шум удален и сохранен в", output_audio_path)
