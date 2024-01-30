import boto3
import os
import subprocess
from botocore.exceptions import BotoCoreError, ClientError

def get_temporary_credentials(assume_role_arn, aws_region, aws_access_key, aws_secret_key):
    """
    Gets temporary credentials from AWS STS.
    """
    if not all([assume_role_arn, aws_region, aws_access_key, aws_secret_key]):
        raise ValueError("Faltan parámetros para obtener credenciales temporales.")

    try:
        sts_client = boto3.client(
            'sts',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        assumed_role = sts_client.assume_role(
            RoleArn=assume_role_arn,
            RoleSessionName="temporary-session"
        )

        credentials = assumed_role['Credentials']
        return {
            'accessKeyId': credentials['AccessKeyId'],
            'secretAccessKey': credentials['SecretAccessKey'],
            'sessionToken': credentials['SessionToken']
        }

    except (BotoCoreError, ClientError) as error:
        raise Exception(f"Error al asumir el rol: {error}")

def load_lambda_layer(layer_name, output_file, assume_role_arn, aws_region, aws_access_key, aws_secret_key):
    """
    Load a layer version of Lambda using AWS CLI.
    """
    if not all([layer_name, output_file, assume_role_arn, aws_region, aws_access_key, aws_secret_key]):
        raise ValueError("Faltan argumentos para cargar la capa de Lambda.")

    try:
        # Obtener credenciales temporales
        temp_credentials = get_temporary_credentials(assume_role_arn, aws_region, aws_access_key, aws_secret_key)

        # Establecer credenciales en el entorno
        os.environ['AWS_ACCESS_KEY_ID'] = temp_credentials['accessKeyId']
        os.environ['AWS_SECRET_ACCESS_KEY'] = temp_credentials['secretAccessKey']
        os.environ['AWS_SESSION_TOKEN'] = temp_credentials['sessionToken']

        # Comando CLI para publicar una versión de capa de Lambda
        aws_cli_command = f"aws lambda publish-layer-version --layer-name {layer_name} --zip-file fileb://{output_file} --compatible-runtimes nodejs18.x --compatible-architectures x86_64"

        # Ejecutar el comando CLI
        subprocess.run(aws_cli_command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("La capa de Lambda se ha cargado con éxito.")
    except (BotoCoreError, ClientError, subprocess.CalledProcessError) as error:
        raise Exception(f"Error al cargar la capa de Lambda: {error}")