import prisma_utils
import aws_utils
import config

def main():
    try:
        # Prisma Cloud Authentication
        token = prisma_utils.authenticate_with_prisma_cloud(config.PRISMA_ACCESS_KEY, config.PRISMA_SECRET_KEY)

        # Getting Defender Layer from Prisma Cloud
        prisma_utils.get_defender_layer(token, config.RUNTIME, config.PROVIDER, config.OUTPUT_FILE)

        # Loading of the Lambda layer using the temporary STS credentials
        temp_credentials = aws_utils.get_temporary_credentials(config.ASSUME_ROLE_ARN, config.AWS_REGION, config.AWS_ACCESS_KEY, config.AWS_SECRET_KEY)
        aws_utils.load_lambda_layer(config.LAYER_NAME, config.OUTPUT_FILE, config.ASSUME_ROLE_ARN, config.AWS_REGION, config.AWS_ACCESS_KEY, config.AWS_SECRET_KEY)


    except Exception as e:
        print(f"Se produjo un error: {e}")

if __name__ == "__main__":
    main()