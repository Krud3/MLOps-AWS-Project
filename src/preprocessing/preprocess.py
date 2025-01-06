import pandas as pd
import boto3
import os
from dotenv import load_dotenv
from io import StringIO
import yaml

# Cargar configuración desde archivo .env
load_dotenv()

# Cargar configuración desde pipeline_config.yaml
with open("../../config/pipeline_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Configuración de S3
s3 = boto3.client('s3')
bucket_name = os.getenv("AWS_S3_BUCKET")

if not bucket_name:
    raise ValueError("La variable AWS_S3_BUCKET no está definida en el archivo .env")

# Descarga de datos desde S3
def load_data_from_s3(input_path):
    key = input_path.replace(f"s3://{bucket_name}/", "")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))

# Cargar datos brutos
data = load_data_from_s3(config['preprocessing']['input_path'])

# ------------------------------------------------------------------------------
# 1. Renombrar columnas:
data.columns = [
    'person_age', 
    'person_gender', 
    'person_education', 
    'person_income', 
    'person_emp_exp', 
    'person_home_ownership',
    'loan_amnt', 
    'loan_intent', 
    'loan_int_rate', 
    'loan_percent_income', 
    'cb_person_cred_hist_length', 
    'credit_score',
    'previous_loan_defaults_on_file', 
    'loan_status'
]


# ------------------------------------------------------------------------------
# Guardar datos (ya con las columnas renombradas) en S3
def save_data_to_s3(df, output_path):
    key = output_path.replace(f"s3://{bucket_name}/", "")
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())

save_data_to_s3(data, config['preprocessing']['output_path'])
print("Preprocesamiento completado y datos guardados en S3.")
