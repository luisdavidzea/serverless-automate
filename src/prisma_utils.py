import requests

def authenticate_with_prisma_cloud(prisma_access_key, prisma_secret_key):
    """
    Authentication with Prisma Cloud and returns a token.
    """
    if not prisma_access_key or not prisma_secret_key:
        raise ValueError("Las credenciales de Prisma Cloud no están configuradas.")

    url = 'https://us-east1.cloud.twistlock.com/us-2-158286553/api/v1/authenticate'
    auth = {
        'username': prisma_access_key,
        'password': prisma_secret_key
    }

    try:
        response = requests.post(url, json=auth)
        response.raise_for_status()
        return response.json().get('token')
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"Error de autenticación HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Error de solicitud: {req_err}")

def get_defender_layer(token, runtime, provider, output_file):
    """
    Obtains a defender layer from Prisma Cloud.
    """
    if not all([token, runtime, provider, output_file]):
        raise ValueError("Uno o más argumentos requeridos están faltando o son inválidos.")

    url = f"https://us-east1.cloud.twistlock.com/us-2-158286553/api/v1/images/twistlock_defender_layer.zip"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "runtime": runtime,
        "provider": provider,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"Bundle descargado exitosamente: {output_file}")
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"Error HTTP al descargar el bundle: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Error de solicitud al descargar el bundle: {req_err}")
    
    