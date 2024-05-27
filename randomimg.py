import requests
import os

# Configuración
NUM_IMAGES = 30
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 300
DESTINATION_FOLDER = "C:/EPP Luciano/Api Detección EPP/imagenesrandom300/imagenesrandom300"

# Función para descargar imágenes aleatorias de Unsplash
def download_random_images(num_images, width, height, destination_folder):
    # URL de la API de Unsplash
    url = f"https://source.unsplash.com/random/{width}x{height}"

    # Crear la carpeta de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Descargar imágenes aleatorias
    for i in range(num_images):
        try:
            # Realizar la solicitud GET para descargar la imagen
            response = requests.get(url)

            # Guardar la imagen en la carpeta de destino con un nombre único
            image_path = os.path.join(destination_folder, f"imagen_{i+1}.jpg")
            with open(image_path, "wb") as f:
                f.write(response.content)

            print(f"Imagen {i+1} descargada correctamente.")

        except Exception as e:
            print(f"Error al descargar la imagen {i+1}: {e}")

# Descargar imágenes aleatorias
download_random_images(NUM_IMAGES, IMAGE_WIDTH, IMAGE_HEIGHT, DESTINATION_FOLDER)
