import os
import boto3
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Obtener variables desde el entorno
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

# Validar variables obligatorias
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_S3_BUCKET:
    raise ValueError("Las variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY y AWS_S3_BUCKET deben estar definidas en el archivo .env.")

# Validar la ruta del directorio data/raw
data_raw_path = "data/raw"
if not os.path.isdir(data_raw_path):
    raise FileNotFoundError(f"El directorio {data_raw_path} no existe o está vacío.")

# Crear cliente de S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID.strip(),
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY.strip(),
    region_name=AWS_REGION.strip(),
)

# Subir los archivos al bucket de S3
def upload_to_s3(local_dir, bucket_name, s3_prefix=""):
    for root, _, files in os.walk(local_dir):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            s3_file_path = os.path.join(s3_prefix, os.path.relpath(local_file_path, local_dir)).replace("\\", "/")

            print(f"Subiendo {local_file_path} a s3://{bucket_name}/{s3_file_path}...")
            s3.upload_file(local_file_path, bucket_name, s3_file_path)

try:
    upload_to_s3(data_raw_path, AWS_S3_BUCKET, "data/raw")
    print("Datos subidos correctamente a S3.")
except Exception as e:
    print(f"Error al subir los datos a S3: {e}")
