import pandas as pd
import pickle
import boto3
import os
from io import BytesIO, StringIO
import yaml
from dotenv import load_dotenv

# Scikit-Learn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neural_network import MLPClassifier

# Cargar configuración
with open("../../config/pipeline_config.yaml", "r") as f:
    config = yaml.safe_load(f)

s3 = boto3.client('s3')
load_dotenv()
bucket_name = os.getenv("AWS_S3_BUCKET")

# ------------------------------------------------------------------------------
# Funciones para cargar/guardar datos/modelos en S3
def load_data_from_s3(dataset_path):
    key = dataset_path.replace(f"s3://{bucket_name}/", "")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))

def save_model_to_s3(model, model_output_path):
    key = model_output_path.replace(f"s3://{bucket_name}/", "")
    buffer = BytesIO()
    pickle.dump(model, buffer)
    s3.put_object(Bucket=bucket_name, Key=key, Body=buffer.getvalue())

# ------------------------------------------------------------------------------
# 1. Cargar datos procesados desde S3
data = load_data_from_s3(config['training']['dataset_path'])

# 2. Separar datos en características (X) y etiqueta (y)
X = data.drop(columns=["loan_status"])
y = data["loan_status"]

# 3. Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# ------------------------------------------------------------------------------
# 4. Definir las columnas numéricas y categóricas (igual que en tu ejemplo)
cat_attribs = [
    'person_gender', 
    'person_education', 
    'person_home_ownership', 
    'loan_intent', 
    'previous_loan_defaults_on_file'
]

num_attribs = [
    'person_age', 
    'person_income', 
    'person_emp_exp', 
    'loan_amnt', 
    'loan_int_rate', 
    'loan_percent_income', 
    'cb_person_cred_hist_length', 
    'credit_score'
]

# 5. Crear pipelines para transformación
cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("cat_encoder", OneHotEncoder(sparse_output=False))
])

num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy='median')),
    ("scaler", StandardScaler())  # o MinMaxScaler()
])

# Combinar en un ColumnTransformer
full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", cat_pipeline, cat_attribs),
])

# ------------------------------------------------------------------------------
# 6. Ajustar el pipeline con los datos de entrenamiento y transformar
X_train_transformed = full_pipeline.fit_transform(X_train)
X_test_transformed  = full_pipeline.transform(X_test)

#to get data
first_row = X_test_transformed[0]
sec_row = X_test_transformed[1]  
print(first_row.tolist())
print(sec_row.tolist())

# ------------------------------------------------------------------------------
# 7. Entrenar el modelo (MLPClassifier).
model = MLPClassifier(
    activation='relu',
    solver='lbfgs',
    alpha=1e-5,
    hidden_layer_sizes=(10,5),
    random_state=123
)

model.fit(X_train_transformed, y_train)

# 8. Evaluar el modelo con cross_val_score (opcional)
scores = cross_val_score(
    model,
    X_train_transformed,
    y_train,
    cv=5,
    scoring='neg_mean_absolute_error'
)
print("CrossVal MAE: ", scores.mean())

# ------------------------------------------------------------------------------
# 9. Predicción sobre conjunto de prueba
y_pred = model.predict(X_test_transformed)

# 10. Métricas
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo en test: {accuracy:.3f}")

# ------------------------------------------------------------------------------
# 11. Guardar modelo en S3
save_model_to_s3(model, config['training']['model_output_path'] + "final_model.pkl")
print("Modelo entrenado y guardado en S3.")
