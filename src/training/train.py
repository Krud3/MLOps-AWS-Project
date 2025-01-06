import pandas as pd
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import boto3
import os
from io import BytesIO, StringIO
import yaml

# Cargar configuración
with open("config/pipeline_config.yaml", "r") as f:
    config = yaml.safe_load(f)

s3 = boto3.client('s3')
bucket_name = os.getenv("AWS_S3_BUCKET")

# Cargar datos procesados desde S3
def load_data_from_s3(dataset_path):
    key = dataset_path.replace(f"s3://{bucket_name}/", "")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))

data = load_data_from_s3(config['training']['dataset_path'])

# Separar datos en características y etiquetas
X = data.drop(columns=["target_column"])
y = data["target_column"]

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo
model = MLPClassifier(
    hidden_layer_sizes=(100, 50),
    max_iter=200,
    activation='relu',
    solver='adam',
    random_state=42
)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy}")

# Guardar modelo en S3
def save_model_to_s3(model, model_output_path):
    key = model_output_path.replace(f"s3://{bucket_name}/", "")
    buffer = BytesIO()
    pickle.dump(model, buffer)
    s3.put_object(Bucket=bucket_name, Key=key, Body=buffer.getvalue())

save_model_to_s3(model, config['training']['model_output_path'] + "final_model.pkl")
print("Modelo entrenado y guardado en S3.")
