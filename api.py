from datetime import datetime
import json
import io
from urllib.parse import unquote
from flask import Blueprint, Flask, config, jsonify, request, abort
import psycopg2
import logging
from function_jwt import validar_token
from auth import routes_auth
from defaults import *
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from googleapiclient.http import MediaIoBaseUpload
from psycopg2.extras import RealDictCursor

ruta_base = Blueprint("ruta_base", __name__)

@ruta_base.before_request
def verify_token_middleware():
    token = request.headers.get('Authorization', '').split(' ')[1]
    logging.info(f"Verifying token: {token}")  # Registro del token
    print(f"Token recibido: {token}")
    response = validar_token(token)
    if response:
        return response

##########################
### METODOS GET ALL DB ###
######### INICIO #########

@ruta_base.route('/all_elements', methods=['GET'])
def get_all_elements():
    """
    Endpoint para obtener todos los elementos.
    :return: JSON con la lista de elementos
    """
    if request.method != 'GET':
        abort(405)  # Método no permitido
    try:
        conn = psycopg2.connect(configdb)
        cursor = conn.cursor()
        cursor.execute('SELECT "ELE_NID", "ELE_CDESCRIPTION" FROM "ELEMENT"')
        elements = cursor.fetchall()
        data = [{'id': e[0], 'description': e[1]} for e in elements]
        cursor.close()
        conn.close()
        return jsonify(data)
    except (psycopg2.Error, Exception) as e:
        print(e)
        app.logger.error(f"Error al obtener elementos: {str(e)}")
        abort(500)  # Error interno del servidor

@ruta_base.route('/all-locations', methods=['GET'])
def get_all_locations():
    """
    Endpoint para obtener todas las ubicaciones.
    :return: JSON con la lista de ubicaciones
    """
    if request.method != 'GET':
        abort(405)  # Método no permitido
    try:
        conn = psycopg2.connect(configdb)
        cursor = conn.cursor()
        cursor.execute('SELECT "LOC_NID", "LOC_CDESCRIPTION" FROM "LOCATION"')
        locations = cursor.fetchall()
        data = [{'id': l[0], 'description': l[1]} for l in locations]
        cursor.close()
        conn.close()
        return jsonify(data)
    except (psycopg2.Error, Exception) as e:
        app.logger.error(f"Error al obtener ubicaciones: {str(e)}")
        abort(500)  # Error interno del servidor

@ruta_base.route('/all-zones', methods=['GET'])
def get_zones():
    """
    Endpoint para obtener todas las zonas.
    :return: JSON con la lista de zonas
    """
    if request.method != 'GET':
        abort(405)  # Método no permitido
    try:
        conn = psycopg2.connect(configdb)
        cursor = conn.cursor()
        cursor.execute('SELECT "Z_NID", "Z_CDESCRIPTION" FROM "ZONE"')
        zones = cursor.fetchall()
        data = [{'id': z[0], 'description': z[1]} for z in zones]
        cursor.close()
        conn.close()
        return jsonify(data)
    except (psycopg2.Error, Exception) as e:
        app.logger.error(f"Error al obtener zonas: {str(e)}")
        abort(500)  # Error interno del servidor

@ruta_base.route('/all-device-types', methods=['GET'])
def get_all_device_types():
    """
    Endpoint para obtener todos los tipos de dispositivos.
    :return: JSON con la lista de tipos de dispositivos
    """
    if request.method != 'GET':
        abort(405)  # Método no permitido
    try:
        conn = psycopg2.connect(configdb)
        cursor = conn.cursor()
        cursor.execute('SELECT "DT_NID", "DT_CNAME" FROM "DEVICE_TYPE"')
        device_types = cursor.fetchall()
        data = [{'id': dt[0], 'name': dt[1]} for dt in device_types]
        cursor.close()
        conn.close()
        return jsonify(data)
    except (psycopg2.Error, Exception) as e:
        app.logger.error(f"Error al obtener tipos de dispositivos: {str(e)}")
        abort(500)  # Error interno del servidor

@ruta_base.route('/all-devices', methods=['GET'])
def get_all_devices():
    """
    Endpoint para obtener todos los dispositivos.
    :return: JSON con la lista de dispositivos
    """
    if request.method != 'GET':
        abort(405)  # Método no permitido
    try:
        
        conn = psycopg2.connect(configdb)
        cursor = conn.cursor()
        cursor.execute('SELECT "DEV_NID", "DEV_CBRAND", "DEV_CMODEL", "DEV_CDEVICE_CODE", "DT_NID_id", "LOC_NID_id", "Z_NID_id" from "DEVICE"')
        devices = cursor.fetchall()
        data = []
        for d in devices:
            device_data = {
                'id': d[0],
                'brand': d[1],
                'model': d[2],
                'location_id': d[3],
                'zone_id': d[4],
                'device_code': d[5],
                'device_type_id': d[6]
            }
            data.append(device_data)
        cursor.close()
        conn.close()
        return jsonify(data)
    except (psycopg2.Error, Exception) as e:
        print(e)
        app.logger.error(f"Error al obtener dispositivos: {str(e)}")
        abort(500)  # Error interno del servidor

@ruta_base.route('/all-sensor-epps', methods=['GET'])
def get_all_sensor_epps():
    """
    Endpoint para obtener todos los sensores EPP.
    :return: JSON con la lista de sensores EPP
    """
    if request.method != 'GET':
        abort(405)  # Método no permitido
    try:
        conn = psycopg2.connect(configdb)
        cursor = conn.cursor()
        cursor.execute('SELECT "SEN_NID", "SEN_FDETECTION_DATE", "SEN_NSTATUS", "SEN_NELEMENT_CODE_1", "SEN_NELEMENT_CODE_2", "SEN_NELEMENT_CODE_3", "SEN_NELEMENT_CODE_4", "SEN_CEVIDENCE", "DEV_NID_id" FROM "SENSOR_EPP"')
        sensor_epps = cursor.fetchall()
        data = []
        for s in sensor_epps:
            sensor_epp_data = {
                'id': s[0],
                'detection_date': s[1],
                'status': s[2],
                'device_id': s[3],
                'element_code_1': s[4],
                'element_code_2': s[5],
                'element_code_3': s[6],
                'element_code_4': s[7],
                'evidence': s[8]
            }
            data.append(sensor_epp_data)
        cursor.close()
        conn.close()
        return jsonify(data)
    except (psycopg2.Error, Exception) as e:
        app.logger.error(f"Error al obtener sensores EPP: {str(e)}")
        abort(500)  # Error interno del servidor

########## FIN ###########
### METODOS GET ALL DB ###
##########################
#---------------------------------------------------------------------------#
##################################
### METODOS GET CON FILTROS DB ###
########### INICIO ###############

@ruta_base.route('/url_alert/<string:name>', methods=["GET"])
def get_url(name):
    """
        Endpoint para obtener la url de una alerta, filtrada por su codigo.
        :return: JSON con la url de la alerta
    """
    if request.method != 'GET':
        abort(405)  # Método no permitido
    if name:
        try:
            conn = psycopg2.connect(configdb)
            cursor = conn.cursor()
            cursor.execute(f'''SELECT "SEN_CEVIDENCE" FROM "SENSOR_EPP" WHERE "SEN_NELEMENT_CODE_1" = '{name}' or "SEN_NELEMENT_CODE_2" = '{name}' or "SEN_NELEMENT_CODE_3" = '{name}' or "SEN_NELEMENT_CODE_4" = '{name}' ''')
            urls = cursor.fetchall()
            data = [{'url': z[0]} for z in urls]
            cursor.close()
            conn.close()
            return jsonify(data)
        except (psycopg2.Error, Exception) as e:
            app.logger.error(f"Error al obtener zonas: {str(e)}")
            abort(500)  # Error interno del servidor+
    else:
        return jsonify({"Error": "Debe enviar un codigo de elemento"}), 400

@ruta_base.route('/url_alert/<string:fecha_1>/<string:fecha_2>/<string:zona>', methods=["GET"])
def get_alert_x_zone(fecha_1, fecha_2, zona):
    try:
        print(fecha_1)
        print(fecha_2)
        print(zona)
        conn = psycopg2.connect(configdb)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = '''
            SELECT "SEN_NID", "SEN_FDETECTION_DATE", "SEN_NSTATUS", "SEN_NELEMENT_CODE_1", "SEN_NELEMENT_CODE_2", 
                   "SEN_NELEMENT_CODE_3", "SEN_NELEMENT_CODE_4", "SEN_CEVIDENCE", "DEV_NID_id", "Z_CDESCRIPTION"
            FROM "SENSOR_EPP" AS sen
            JOIN "DEVICE" AS dev ON sen."DEV_NID_id" = dev."DEV_NID"
            JOIN "ZONE" AS zn ON zn."Z_NID" = dev."Z_NID_id"
            WHERE "SEN_FDETECTION_DATE" BETWEEN %s AND %s
            AND zn."Z_CDESCRIPTION" = %s
        '''
        
        cursor.execute(query, (fecha_1, fecha_2, zona))
        alertas = cursor.fetchall()
        
        data = [{'Id': alerta['SEN_NID'], 
                 'Fecha_deteccion': alerta['SEN_FDETECTION_DATE'], 
                 'Estado': alerta['SEN_NSTATUS'],
                 'Elemento_1': alerta['SEN_NELEMENT_CODE_1'],
                 'Elemento_2': alerta['SEN_NELEMENT_CODE_2'],
                 'Elemento_3': alerta['SEN_NELEMENT_CODE_3'],
                 'Elemento_4': alerta['SEN_NELEMENT_CODE_4'],
                 'Evidencia': alerta['SEN_CEVIDENCE'],
                 'Dispositivo_Id': alerta['DEV_NID_id'],
                 'Zona': alerta['Z_CDESCRIPTION'],
                 } for alerta in alertas]
        
        cursor.close()
        conn.close()
        return jsonify(data)
    
    except (psycopg2.Error, Exception) as e:
        app.logger.error(f"Error al obtener zonas: {str(e)}")
        abort(500)  # Error interno del servidor

############# FIN ################
### METODOS GET CON FILTROS DB ###
##################################
#---------------------------------------------------------------------------#
##################################
### GUARDAR REGISTROS EN DRIVE ###
############# INICIO #############
# La función `upload_to_drive` se encarga de subir archivos a Google Drive.
# Recibe como parámetros el archivo a subir, el ID de la carpeta donde se guardará y el nombre del archivo.
# Utiliza credenciales de una cuenta de servicio para autenticarse en la API de Google Drive.
# Crea metadatos para el archivo, incluyendo su nombre y, opcionalmente, la carpeta padre.
# Prepara el cuerpo del medio del archivo para la subida, especificando el tipo de contenido.
# Realiza la solicitud para crear el archivo en Drive y captura la respuesta.
# Configura los permisos del archivo para que sea accesible públicamente.
# Devuelve el enlace público del archivo si la subida es exitosa, de lo contrario, devuelve None en caso de error.

def upload_to_drive(file, folder_id, filename):
    try:
        credentials_path = r'C:\inetpub\wwwroot\Api-deteccion-EPP\neuronia-422721-4827a76feb12.json'
        creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=['https://www.googleapis.com/auth/drive']
        )
        drive_service = build('drive', 'v3', credentials=creds)
        file_metadata = {'name': filename}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        media_body = MediaIoBaseUpload(file.stream, mimetype=file.mimetype)
        file = drive_service.files().create(
            body=file_metadata, media_body=media_body, fields='id, webViewLink'
        ).execute()

        # Configurar los permisos del archivo para hacerlo público
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        drive_service.permissions().create(
            fileId=file['id'],
            body=permission,
            fields='id'
        ).execute()

        public_link = file.get('webViewLink')
        id_file = file.get('id')
        webContentLink = file.get('webContentLink')
        print(f'File uploaded. Public link: {public_link}')
        print(f'File uploaded. id: {id_file}')
        return public_link, id_file
    except Exception as e:
        print(e)
        return None

def guardar_archivo(file, filename, folder_id):
    if file:
        # Obtener la extensión del archivo del objeto file
        file_extension = file.filename.rsplit('.', 1)[1].lower()

        # Validar la extensión del archivo
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov','json']
        if file_extension not in allowed_extensions:
            print(f"Extensión '{file_extension}' no permitida.")
            return None

        # Validar el tamaño máximo del archivo (por ejemplo, 50MB)
        max_size = 50 * 1024 * 1024
        if file.content_length > max_size:
            print(f"Tamaño del archivo ({file.content_length}) excede el máximo permitido.")
            return None

        # Subir el archivo a Google Drive
        public_link, id_file = upload_to_drive(file, folder_id, filename)
        if public_link is None:
            print("Error al subir el archivo a Google Drive.")
            return None
        return public_link, id_file
    return None

# La función 'sensor_epp' maneja las solicitudes POST para la ruta '/sensor_epp/<string:filename>'
# Esta función es responsable de procesar los datos y archivos enviados a través de la solicitud HTTP.
# Se espera que la solicitud contenga un campo 'data' en formato JSON y un archivo en el campo 'evidence'.

# 1. Imprime la solicitud completa, el formulario y los archivos recibidos para depuración.
# 2. Verifica si el campo 'data' está presente en el formulario. Si no, retorna un error 400.
# 3. Intenta parsear el campo 'data' como JSON. Si falla, retorna un error 400 indicando que el JSON no es válido.
# 4. Verifica si hay información en alguno de los campos 'element_code' del JSON.
# 5. Si se recibe información válida, asigna la fecha y hora actual.
# 6. Extrae los valores necesarios del JSON para su uso posterior.
# 7. Verifica que el 'device_id' sea un entero. Si no, retorna un error 400.
# 8. Si se proporcionó un archivo en 'evidence', intenta guardar el archivo en Google Drive usando la función 'guardar_archivo'.
# 9. Si el archivo no es válido o no se pudo guardar, retorna un error 400.
# 10. Finalmente, si todo es correcto, retorna el enlace público del archivo guardado en Google Drive.

@ruta_base.route('/sensor_epp/<string:filename>', methods=["POST"])
def sensor_epp(filename):
    try:
        print(request)
        print(request.form)
        print(request.files)
        # Verificar si se proporcionó el campo "data" en la solicitud
        if "data" not in request.form:
            return jsonify({"Message": "El campo 'data' es requerido"}), 400

        input_data = request.form["data"]
        file = request.files.get("evidence")
        print(input_data)

        if input_data and filename:
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError:
                return jsonify({"Message": "El campo 'data' debe ser una cadena JSON válida"}), 400

            status = False
            # Validar si alguno de los element_code tiene información
            for i in range(1, 5):
                element_code = input_data.get(f"element_code_{i}")
                if element_code:
                    status = True
                    break

            # Asignar la fecha y hora actual si se recibió información
            detection_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Obtener los valores necesarios para la inserción en la base de datos
            device_id = input_data.get("device_id")
            element_code_1 = input_data.get("element_code_1")
            element_code_2 = input_data.get("element_code_2")
            element_code_3 = input_data.get("element_code_3")
            element_code_4 = input_data.get("element_code_4")

            # Validar que device_id sea un entero
            if not isinstance(device_id, int):
                return jsonify({"Message": "El campo 'device_id' debe ser un entero"}), 400

            # Guardar el archivo en Drive
            evidence_path = None
            folder_id = '1W1C-8LHz8FI1KkbACicfXVZzKLKsRHBR'
            if file:
                evidence_path, id_file = guardar_archivo(file, filename, folder_id)
                if evidence_path is None:
                    return jsonify({"Message": "Archivo no válido"}), 400
            else:
                print("No se proporcionó un archivo 'evidence'")

            conn = psycopg2.connect(configdb)
            cur = conn.cursor()

            # Insertar los datos en la base de datos según el valor de status
            if status:
                cur.execute(
                    '''INSERT INTO "SENSOR_EPP"("DEV_NID_id", "SEN_FDETECTION_DATE", "SEN_NSTATUS", "SEN_NELEMENT_CODE_1", "SEN_NELEMENT_CODE_2", "SEN_NELEMENT_CODE_3", "SEN_NELEMENT_CODE_4", "SEN_CEVIDENCE", "SEN_CEVIDENCE_DRIVE_ID") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (device_id, detection_date, status, element_code_1, element_code_2, element_code_3, element_code_4, evidence_path, id_file)
                )
            else:
                cur.execute(
                    '''INSERT INTO "SENSOR_EPP"("DEV_NID_id", "SEN_FDETECTION_DATE", "SEN_NSTATUS") VALUES (%s, %s, %s)''',
                    (device_id, detection_date, status)
                )

            conn.commit()
            cur.close()
            conn.close()

            # Agregar las variables status y detection_date a la respuesta
            response_data = {
                "Message": "OK recibido",
                "info": input_data,
                "status": status,
                "detection_date": detection_date,
                "evidence_path": evidence_path
            }
            return jsonify(response_data), 201
        else:
            return jsonify({"Message": "Bad Request"}), 400
    except Exception as e:
        print("ERROR", str(e))
        return jsonify({"ERROR": str(e)}), 400

@ruta_base.route('/sensor_json_epp', methods=["POST"])
def sensor_json_epp():
    try:
        conn = psycopg2.connect(configdb)
        cur = conn.cursor()
        # Recibe el archivo JSON
        data = request.form["data"]
        print(request.files)
        
        # Verifica que el archivo no esté vacío
        if not data:
            return jsonify({'error': 'El archivo JSON está vacío'}), 400
        else:
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return jsonify({"Message": "El campo 'data' debe ser una cadena JSON válida"}), 400
        
        # Obtenemos la imagen (opcional)
        try:
            file = request.files.get("evidence")
        except Exception as e:
            file = ''

        # Convierte el JSON a un archivo en memoria
        # json_file = io.BytesIO(json.dumps(data).encode('utf-8'))
        
        # Obtiene la longitud del archivo JSON
        # length = len(data)
        # if length > 40:
        #     estado = 1
        # else:
        #     estado = 0
        estado = 1

        prediction = '' # en caso de que sea un solo elemento
        predictions = [] # en caso de que sean 2 elementos

        filename = data['image_name']
        zona = data['zone']
        if data['prediction'].__contains__(' Y '):
            predictions = data['prediction'].split(' Y ')
        else:
            prediction = data['prediction']
            


        if len(predictions) > 1:
            # Transforma la lista
            transformed = ', '.join([f"upper('{item}')" for item in predictions])
            cur.execute(f'''SELECT "ELE_NID" FROM "ELEMENT" WHERE upper("ELE_CDESCRIPTION") in ({transformed}) ''')
            response = cur.fetchall()
            dato = [z[0] for z in response]
        else:
            cur.execute(f'''SELECT "ELE_NID" FROM "ELEMENT" WHERE upper("ELE_CDESCRIPTION") = upper('{prediction}') ''')
            response = cur.fetchone()
            dato = [response]

        var1, var2, var3, var4 = assign_values(dato)
        
        folder_id = '1W1C-8LHz8FI1KkbACicfXVZzKLKsRHBR' # Carpeta Json
        if file:
            evidence_path, id_file = guardar_archivo(file, filename, folder_id)
            if evidence_path is None:
                return jsonify({"Message": "Archivo no válido"}), 400
        else:
            print("No se proporcionó un archivo 'evidence'")


        # evidence_path, id_file = guardar_archivo(json_file, filename, folder_id)
        # Asignar la fecha y hora actual si se recibió información
        detection_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extrae las predicciones
        # predictions = [item['prediction'] for item in data]
        
        if evidence_path and id_file:
            
            cur.execute(
                '''INSERT INTO "SENSOR_EPP"("DEV_NID_id", "SEN_FDETECTION_DATE", "SEN_NSTATUS", "SEN_NELEMENT_CODE_1_id", "SEN_NELEMENT_CODE_2_id", "SEN_NELEMENT_CODE_3_id", "SEN_NELEMENT_CODE_4_id", "SEN_CEVIDENCE", "SEN_CEVIDENCE_DRIVE_ID") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (1, detection_date, True, var1, var2, var3, var4, evidence_path, id_file)
            )

        conn.commit()
        cur.close()
        conn.close()
        # Agregar las variables status y detection_date a la respuesta
        response_data = {
            "Message": "OK recibido",
            "info": 'Json subido correctamente',
            "status": 'OK',
            "detection_date": detection_date,
            "evidence_path": evidence_path
        }
        return jsonify(response_data), 201

    except Exception as e:
        print(e)
        # Agregar las variables status y detection_date a la respuesta
        response_data = {
            "Message": "Error al subir archivo",
            "info": str(e),
            "status": 'ERROR'
        }
        return jsonify(response_data), 400


@ruta_base.route('/log', methods=["POST"])
def log_api():
    try:
        conn = psycopg2.connect(configdb)
        cur = conn.cursor()
        # Recibe el archivo JSON
        data = request.form['data']
        # Verifica que el archivo no esté vacío
        if not data:
            return jsonify({'error': 'El archivo JSON está vacío'}), 400
        else:
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return jsonify({"Message": "El campo 'data' debe ser una cadena JSON válida"}), 400
        
        fecha = data['detection_date']
        respuesta = data['message']

        try:
            cur.execute(
                '''INSERT INTO "LOG_API"("LOG_RESPUESTA", "LOG_FDETECTION_DATE" ) VALUES (%s, %s)''',
                (respuesta, fecha)
            )
            conn.commit()
            cur.close()
            conn.close()
            # Agregar las variables status y detection_date a la respuesta
            response_data = {
                "Message": "Recibido",
                "info": 'Hertbeat recibido por API',
                "status": 'OK'
            }
            return jsonify(response_data), 201
        except Exception as e:
            print(e)
            # Agregar las variables status y detection_date a la respuesta
            response_data = {
                "Message": "Error",
                "info": 'Error al guardar Hertbeat',
                "status": 'error',
                "exception":str(e)
            }
            return jsonify(response_data), 400

    except Exception as e:
        print(e)
        # Agregar las variables status y detection_date a la respuesta
        response_data = {
            "Message": "Error 1",
            "info": 'Error al guardar Hertbeat',
            "status": 'error',
            "exception":str(e)
        }
        return jsonify(response_data), 400

def assign_values(lst):
    # Extiende la lista con ceros hasta que tenga una longitud de 4
    while len(lst) < 4:
        lst.append(None)
    
    # Asigna los valores a las variables
    var1, var2, var3, var4 = lst[:4]
    
    return var1, var2, var3, var4

############### FIN ##############
### GUARDAR REGISTROS EN DRIVE ###
##################################

app = Flask(__name__)

app.register_blueprint(routes_auth)
app.register_blueprint(ruta_base)

logging.basicConfig(filename='app.log', level=logging.DEBUG)

if __name__ == '__main__':
    app.run(debug=True,port=9000)