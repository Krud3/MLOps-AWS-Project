import subprocess

def execute_stage(command, stage_name):
    try:
        print(f"Ejecutando la etapa: {stage_name}...")
        subprocess.run(command, shell=True, check=True)
        print(f"Etapa {stage_name} completada exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error en la etapa {stage_name}: {e}")
        exit(1)

def main():
    # Etapas del pipeline
    stages = [
        {"name": "Preprocesamiento", "command": "python src/preprocessing/preprocess.py"},
        {"name": "Entrenamiento", "command": "python src/training/train.py"},
        {"name": "Despliegue", "command": "python src/deployment/deploy.py"},
    ]

    # Ejecutar cada etapa
    for stage in stages:
        execute_stage(stage["command"], stage["name"])

    print("Pipeline ejecutado exitosamente.")

if __name__ == "__main__":
    main()
