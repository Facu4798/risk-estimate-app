#set working directory to current file
import sys
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv("app.env"))
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def salir_container():
    print("Deteniendo contenedor...")
    # os.system("docker stop fastapi-container2")
    # os.system("docker rm fastapi-container2")
    os.system(os.getenv("DOCKER_STOP"))
    os.system(os.getenv("DOCKER_RM"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    import requests
    # Iniciar el contenedor
    print("Iniciando contenedor de la API...")
    # os.system("docker run -d -p 8000:80 --name fastapi-container2 final")
    os.system(os.getenv("DOCKER_RUN"))
    import time
    time.sleep(2)  
    try:
        #response = requests.get("http://localhost:8000/last-prediction")
        response = requests.get(os.getenv("API_URL"))
        print(response)
        if response.status_code != 200:
            return jsonify({"error": "No se encontraron datos"}), 404
        datos_api = response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    def prediction_hash(p) -> str:
        import numpy as np
        return str(np.round(float(p), 2)) + "%"

    datos_api["5Days"] = prediction_hash(datos_api["5Days"])
    datos_api["10Days"] = prediction_hash(datos_api["10Days"])
    datos_api["30Days"] = prediction_hash(datos_api["30Days"])

    print("Ejecutando limpieza...")
    salir_container()

    return jsonify(datos_api)

if __name__ == "__main__":
    print("Iniciando aplicación Flask...")
    app.run(debug=True, host="0.0.0.0")
 
