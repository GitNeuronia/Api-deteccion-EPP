from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from flask import jsonify
from defaults import *
# Función para calcular la fecha de expiración del token basada en la cantidad de días proporcionados
def tiempo_expiracion(days: int):
    hoy = datetime.now()
    fecha_exp = hoy + timedelta(days)
    return fecha_exp

# Función para crear un token JWT con los datos proporcionados y una fecha de expiración
def escribir_token(data: dict):
    try:
        token = encode(payload={**data, "exp": tiempo_expiracion(180)}, key=apisecret, algorithm="HS256")
        return token
    except Exception as e:
        response = jsonify({"message": "No se puede crear el token", "error": str(e)})
        response.status_code = 401
        return response

# Función para validar un token JWT y opcionalmente devolver los datos decodificados si output es True
def validar_token(token):
    try:
        decode(token, key=apisecret, algorithms=["HS256"])
        print(decode)
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response
