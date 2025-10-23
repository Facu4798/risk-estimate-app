import sys
import os
import dotenv

# Cargar variables de entorno
dotenv.load_dotenv(dotenv.find_dotenv("app.env"))
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask import Flask, render_template, jsonify
import requests
import numpy as np

app = Flask(__name__)

# Configuración
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_INSTANCE = os.getenv("DATABRICKS_INSTANCE")
ENDPOINT_NAME = "arima-30d-api"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    """Obtiene predicciones de Databricks para 5, 10 y 30 días"""
    try:
        url = f"{DATABRICKS_INSTANCE}/serving-endpoints/{ENDPOINT_NAME}/invocations"
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"dataframe_records": [{}]}
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"ERROR: API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return jsonify({"error": f"Error en API: {response.status_code}"}), 500
        
        data = response.json()
        
        # Extraer predicciones (maneja múltiples formatos de respuesta)
        predictions = None
        if "predictions" in data:
            predictions = data["predictions"][0] if isinstance(data["predictions"], list) else data["predictions"]
        elif all(k in data for k in ["5", "10", "30"]):
            predictions = data
        
        if not predictions:
            print(f"ERROR: Cannot extract predictions from: {data}")
            return jsonify({"error": "Formato de respuesta inválido"}), 500
        
        # Convertir a porcentajes
        def to_percentage(val):
            try:
                return f"{np.round(float(val) * 100, 2)}%"
            except:
                return "N/A"
        
        return jsonify({
            "5Days": to_percentage(predictions.get("5", 0)),
            "10Days": to_percentage(predictions.get("10", 0)),
            "30Days": to_percentage(predictions.get("30", 0))
        })
    
    except requests.exceptions.Timeout:
        print("ERROR: Request timeout")
        return jsonify({"error": "Timeout al conectar"}), 504
    
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Connection error - {e}")
        return jsonify({"error": "Error de conexión"}), 503
    
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "configured": bool(DATABRICKS_TOKEN and DATABRICKS_INSTANCE)
    })

if __name__ == "__main__":
    if not DATABRICKS_TOKEN or not DATABRICKS_INSTANCE:
        print("ERROR: Missing environment variables")
    else:
        print(f"Starting Flask app - Endpoint: {ENDPOINT_NAME}")
    
    app.run(debug=False)


