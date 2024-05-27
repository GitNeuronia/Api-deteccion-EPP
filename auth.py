from venv import logger
from flask import Blueprint,request,jsonify
from function_jwt import escribir_token, validar_token
import requests
import re
routes_auth = Blueprint("routes_auth",__name__)
URL_AUTH = 'http://127.0.0.1:8000/login/'
@routes_auth.route("/login",methods = ["POST"])
# Este bloque de código maneja la autenticación y generación de tokens JWT para usuarios
# Verifica si el usuario es CIROS con contraseña específica para autenticación directa
# Si no, intenta autenticar usando un servicio externo Django con CSRF y manejo de errores

def login():
    data = request.get_json()
    if data['username'] == "CIROS":
        if data['password'] == "Ciros.2023":
            return escribir_token(data = request.get_json())
        else:
            response = jsonify({"message":"invalid credentials"})
            response.status_code = 404
            return response
    else:
        username = data['username']
        password = data['password']
                
        # Realiza una solicitud GET a la página que contiene el formulario
        response_get = requests.get(URL_AUTH)       
        # Extrae el token CSRF del HTML de la página
        csrf_token_match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', response_get.text)
        if csrf_token_match:
            csrf_token = csrf_token_match.group(1)
            
            # Enviar la solicitud POST a Django con el token CSRF
            headers = {'X-CSRFToken': csrf_token}
            payload = {'username': username, 'password': password, 'csrfmiddlewaretoken':csrf_token}
            cookies = {'csrftoken': csrf_token}
            response_post = requests.post(URL_AUTH, data=payload, headers=headers,cookies=cookies)

            # Verificar la respuesta de Django
            if response_post.status_code == 200:
                error_matches = re.findall(r"Swal\.fire\(\{[^}]*text: ['\"](.*?)['\"][^}]*\}\)", response_post.text)
                if error_matches:
                    response = jsonify({"message":"invalid credentials"})
                    response.status_code = 404
                    return response

                # El usuario está autenticado en Django
                return escribir_token(data = request.get_json())

            # Si la autenticación falla en Django, manejar el error
            response = jsonify({"message":"invalid credentials"})
            response.status_code = 404
            return response
        else:
            return jsonify({'error': 'CSRF token not found in HTML'})

