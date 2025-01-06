import pandas as pd
import boto3
import os
from io import StringIO
import yaml

# Cargar configuración
with open("config/pipeline_config.yaml", "r") as f:
    config = yaml.safe_load(f)

s3 = boto3.client('s3')
bucket_name = os.getenv("AWS_S3_BUCKET")

# Descarga de datos desde S3
def load_data_from_s3(input_path):
    key = input_path.replace(f"s3://{bucket_name}/", "")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))

# Cargar datos
data = load_data_from_s3(config['preprocessing']['input_path'])

# Transformaciones específicas según el notebook
data.dropna(subset=['important_column'], inplace=True)  # Manejo de valores faltantes específicos
data['new_feature'] = data['existing_feature'] ** 2  # Crear nuevas columnas o transformaciones

# Guardar datos procesados en S3
def save_data_to_s3(df, output_path):
    key = output_path.replace(f"s3://{bucket_name}/", "")
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())

save_data_to_s3(data, config['preprocessing']['output_path'])
print("Preprocesamiento completado y datos guardados en S3.")
