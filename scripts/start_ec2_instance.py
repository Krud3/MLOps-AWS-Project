import boto3
import os
from dotenv import load_dotenv

# Cargar configuración desde .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
AWS_AMI_ID = os.getenv("AWS_AMI_ID")
AWS_KEY_NAME = os.getenv("AWS_KEY_NAME")
AWS_SECURITY_GROUP = os.getenv("AWS_SECURITY_GROUP", "mlops-security-group")
AWS_EC2_INSTANCE_TYPE = os.getenv("AWS_EC2_INSTANCE_TYPE", "t2.micro")

# Crear cliente EC2
ec2 = boto3.client(
    "ec2",
    aws_access_key_id=AWS_ACCESS_KEY_ID.strip(),
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY.strip(),
    region_name=AWS_REGION.strip(),
)

def start_ec2_instance():
    try:
        print("Iniciando instancia EC2...")
        response = ec2.run_instances(
            ImageId=AWS_AMI_ID.strip(),
            InstanceType=AWS_EC2_INSTANCE_TYPE.strip(),
            KeyName=AWS_KEY_NAME.strip(),
            SecurityGroups=[AWS_SECURITY_GROUP.strip()],
            MinCount=1,
            MaxCount=1,
        )
        instance_id = response["Instances"][0]["InstanceId"]
        print(f"Instancia EC2 iniciada: {instance_id}")

        # Guardar el ID de la instancia en un archivo temporal
        with open("ec2_instance_id.txt", "w") as f:
            f.write(instance_id)
        return instance_id
    except Exception as e:
        print(f"Error al iniciar la instancia EC2: {e}")
        exit(1)

if __name__ == "__main__":
    instance_id = start_ec2_instance()
    print(f"Instancia EC2 creada con ID: {instance_id}")
