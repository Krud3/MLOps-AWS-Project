#!/bin/bash

# Configuración de variables desde el .env
source ../.env

# Ejecutar las etapas del pipeline
echo "Ejecutando pipeline..."

python ../src/preprocessing/preprocess.py
if [ $? -ne 0 ]; then
  echo "Error en la etapa de preprocesamiento."
  exit 1
fi

python ../src/training/train.py
if [ $? -ne 0 ]; then
  echo "Error en la etapa de entrenamiento."
  exit 1
fi

python ../src/deployment/deploy.py
if [ $? -ne 0 ]; then
  echo "Error en la etapa de despliegue."
  exit 1
fi

echo "Pipeline ejecutado exitosamente."
