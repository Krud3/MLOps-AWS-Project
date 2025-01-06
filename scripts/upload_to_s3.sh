#!/bin/bash

# Configuración de variables desde el .env
source ../.env

# Subir datos al bucket de S3
echo "Subiendo datos a S3..."
aws s3 cp ../data/raw/ s3://$AWS_S3_BUCKET/${PIPELINE_RAW_DATA_PREFIX:-data/raw/} --recursive

if [ $? -eq 0 ]; then
  echo "Datos subidos correctamente a S3."
else
  echo "Error al subir los datos a S3."
fi
