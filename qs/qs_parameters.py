# Se necesita 'os' para obtener las variables de entorno
# y load_dotenv para cargar el archivo .env especifico
import os
from dotenv import load_dotenv # pip install python-dotenv

def getParameters(ENV_FILE_PATH):
    load_dotenv(ENV_FILE_PATH)

    # Creamos un diccionario con todos los parametros
    params = {
        "sb_environment_param": os.environ.get("SB_ENVIRONMENT_PARAM"), 
        "sb_country_param": os.environ.get("SB_COUNTRY_PARAM")
    }

    return params