import pickle
import boto3
import os
from io import BytesIO
import yaml

# Cargar configuración
with open("config/pipeline_config.yaml", "r") as f:
    config = yaml.safe_load(f)

s3 = boto3.client('s3')
bucket_name = os.getenv("AWS_S3_BUCKET")

# Cargar modelo desde S3
def load_model_from_s3(model_path):
    key = model_path.replace(f"s3://{bucket_name}/", "")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    buffer = BytesIO(response['Body'].read())
    return pickle.load(buffer)

model = load_model_from_s3(config['deployment']['model_path'])
print("Modelo cargado para despliegue.")

# Simular despliegue
print(f"Modelo desplegado en endpoint: {config['deployment']['endpoint_name']}")
