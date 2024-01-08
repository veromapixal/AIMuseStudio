import cv2
import rembg


def remove_background(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Создаем VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # или используйте другой кодек, поддерживаемый вашей системой
    video_writer = cv2.VideoWriter(output_path, fourcc, 30, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Преобразование кадра в формат RGBA
        rgba_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        print("преобразовано")
        # Удаление фона из кадра
        alpha_matte = rembg.remove(rgba_frame)
        print("удалён фон")
        # Преобразование кадра и альфа-маты в формат BGR
        result_frame = cv2.cvtColor(alpha_matte, cv2.COLOR_RGBA2BGR)
        print("преобразовано")
        # Запись обработанного кадра
        video_writer.write(result_frame)
        print("кадр записан")
    cap.release()
    video_writer.release()


if __name__ == "__main__":
    input_video_path = "video_2.mp4"
    output_video_path = "output_video_no_bg.mp4"

    remove_background(input_video_path, output_video_path)
