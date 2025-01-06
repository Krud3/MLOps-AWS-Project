#!/bin/bash

# Configuración de variables desde el .env
source ../.env

# Iniciar instancia EC2
echo "Iniciando instancia EC2..."
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id $AWS_AMI_ID \
  --count 1 \
  --instance-type $AWS_EC2_INSTANCE_TYPE \
  --key-name $AWS_KEY_NAME \
  --security-groups $AWS_SECURITY_GROUP \
  --query "Instances[0].InstanceId" \
  --output text)

if [ $? -eq 0 ]; then
  echo "Instancia EC2 iniciada: $INSTANCE_ID"
else
  echo "Error al iniciar la instancia EC2."
fi

# Guardar el ID de la instancia en un archivo temporal
echo $INSTANCE_ID > ../ec2_instance_id.txt
