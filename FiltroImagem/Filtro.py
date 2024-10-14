import threading
from PIL import Image, ImageFilter
import time
import sys
from datetime import datetime
import pytz

LOCAL_TIMEZONE = pytz.timezone('America/Recife')

def get_local_time():
    utc_time = datetime.now(pytz.utc)
    local_time = utc_time.astimezone(LOCAL_TIMEZONE)
    return local_time.strftime('%H:%M:%S')

def apply_filter(image_path, output_path, filter_func):
    try:
        print(f"{get_local_time()} - {threading.current_thread().name} - Iniciando processamento da imagem: {image_path}")
        sys.stdout.flush()

        image = Image.open(image_path)
        filtered_image = image.filter(filter_func)
        filtered_image.save(output_path)

        print(f"{get_local_time()} - {threading.current_thread().name} - Imagem processada e salva em: {output_path}")
        sys.stdout.flush()

    except Exception as e:
        print(f"{get_local_time()} - {threading.current_thread().name} - Erro ao processar a imagem: {e}")
        sys.stdout.flush()

def main():
    image1_path = "imagem1.png"
    image2_path = "imagem2.png"
    output1_path = "imagem1_blur.png"
    output2_path = "imagem2_blur.png"

    filter_func = ImageFilter.BLUR

    start_time = time.time()

    print(f"{get_local_time()} - MainThread - Iniciando processamento em paralelo das imagens.")
    sys.stdout.flush()

    thread1 = threading.Thread(target=apply_filter, args=(image1_path, output1_path, filter_func), name="Thread-1")
    thread2 = threading.Thread(target=apply_filter, args=(image2_path, output2_path, filter_func), name="Thread-2")

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    total_time = time.time() - start_time
    print(f"{get_local_time()} - MainThread - Tempo total de processamento: {total_time:.2f} segundos")
    sys.stdout.flush()

if __name__ == "__main__":
    main()