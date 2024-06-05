
# Este bloque de código se encarga de realizar una solicitud POST a un servidor local
# Se define la URL del servidor al que se hará la solicitud
# Se prepara el payload que contiene los datos en formato JSON
# Se especifica la ruta del archivo que se enviará como parte de la solicitud
# Se configura el archivo y su tipo de contenido para ser enviado
# Se establecen los headers de la solicitud, incluyendo un token de autorización
# Se registra el tiempo de inicio de la solicitud
# Se realiza la solicitud POST con los datos, archivos y headers configurados
# Se registra el tiempo de finalización de la solicitud
# Se calcula el tiempo de respuesta de la solicitud
# Se imprimen el tiempo de respuesta y la respuesta de la API



import requests
import time

url = "http://localhost:5000/sensor_json_epp"

payload = {
    'data': '{"image_name": "frame_28800.jpg", "prediction": "CASCO Y CHALECO", "confidence": 0.9252026081085205, "zone": 1}'
}
file_path = r"C:\EPP Luciano\Api Deteccion EPP\imagenesrandom300\img_prueba.jpg"
files = [('evidence', ('img_prueba.jpg', open(file_path, 'rb'), 'application/octet-stream'))]
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJhZG1pbiIsImV4cCI6MTczMjAxMTUzOX0.Q_agNZdGDXkWVpCw7V8fHh6VCNsNILmpTZVsBn9u098',
}

start_time = time.time()
response = requests.post(url, headers=headers, data=payload, files=files)
end_time = time.time()

response_time = end_time - start_time

print("Response time:", response_time)
print("Response API:",response.text)