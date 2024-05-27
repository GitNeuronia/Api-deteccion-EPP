import requests
import os

# Configuración
NUM_VIDEOS = 10
VIDEO_DURATION = 5  # Duración en segundos
DESTINATION_FOLDER = "C:/EPP Luciano/Api Detección EPP/videorandom5"

# Función para descargar videos aleatorios de Pexels
def download_random_videos(num_videos, duration, destination_folder):
    # URL de la API de Pexels con un parámetro de consulta "query"
    url = f"https://api.pexels.com/videos/search?query=random&per_page={num_videos}&min_duration={duration}&max_duration={duration}"


    # Clave de API de Pexels (necesitas registrarte en Pexels para obtener una)
    api_key = "VzROnrhfohHQJF2WQiSnhsdvY6rF2bUBwReD2FD86TLjUkAgdncKrnhB"

    # Encabezados de la solicitud con la clave de la API
    headers = {"Authorization": api_key}
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Descargar videos aleatorios
    try:
        response = requests.get(url, headers=headers)

        print("URL de la solicitud:", response.url)  # Imprimir la URL de la solicitud
        print("Respuesta de la API:", response.text)  # Imprimir la respuesta de la API (JSON)
    
        data = response.json()

        for idx, video_data in enumerate(data["videos"], start=1):
            video_url = video_data["video_files"][0]["link"]

            # Descargar el video
            video_response = requests.get(video_url)

            # Guardar el video en la carpeta de destino con un nombre único
            video_path = os.path.join(destination_folder, f"video_{idx}.mp4")
            with open(video_path, "wb") as f:
                f.write(video_response.content)

            print(f"Video {idx} descargado correctamente.")

    except Exception as e:
        print(f"Error al descargar videos: {e}")

# Descargar videos aleatorios
download_random_videos(NUM_VIDEOS, VIDEO_DURATION, DESTINATION_FOLDER)
