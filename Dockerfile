# Imagen base
FROM python:3.8-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos del proyecto al contenedor
COPY . .

# Establecer las variables de entorno (asegúrate de tener el archivo .env configurado correctamente)
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_REGION=$AWS_REGION

# Comando predeterminado para ejecutar el pipeline
CMD ["bash", "./scripts/deploy_pipeline.sh"]
