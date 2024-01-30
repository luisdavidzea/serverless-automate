import os
from dotenv import load_dotenv

load_dotenv()

PRISMA_ACCESS_KEY = os.environ.get('PRISMA_ACCESS_KEY')
PRISMA_SECRET_KEY = os.environ.get('PRISMA_SECRET_KEY')

RUNTIME = os.environ.get('RUNTIME')
PROVIDER = os.environ.get('PROVIDER')
OUTPUT_FILE = os.environ.get('OUTPUT_FILE')

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
ASSUME_ROLE_ARN = os.environ.get('ASSUME_ROLE_ARN')

NEW_HANDLER = os.environ.get('NEW_HANDLER')
LAMBDA_FUNCTION_NAME = os.environ.get('LAMBDA_FUNCTION_NAME')
LAYER_NAME = os.environ.get('LAYER_NAME')