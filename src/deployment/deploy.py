import pickle
import boto3
import os
from flask import Flask, request, jsonify
from io import BytesIO
import yaml
import subprocess

from dotenv import load_dotenv

# Cargar configuración
with open("../../config/pipeline_config.yaml", "r") as f:
    config = yaml.safe_load(f)

load_dotenv()
s3 = boto3.client('s3')
bucket_name = os.getenv("AWS_S3_BUCKET")

# Cargar modelo desde S3
def load_model_from_s3(model_path):
    key = model_path.replace(f"s3://{bucket_name}/", "")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    buffer = BytesIO(response['Body'].read())
    return pickle.load(buffer)

# Configurar servidor Flask
app = Flask(__name__)
model = load_model_from_s3(config['deployment']['model_path'])
print("Modelo cargado exitosamente.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        predictions = model.predict([data['features']])
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Configurar la instancia EC2 si es necesario
    instance_type = config['deployment']['instance_type']
    endpoint_name = config['deployment']['endpoint_name']

    # Ejecutar el servidor Flask
    app.run(host='0.0.0.0', port=5000)
    print(f"Endpoint {endpoint_name} ejecutándose en el puerto 5000.")
