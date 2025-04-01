import boto3
import os
import time
import traceback
import base64

class S3Uploader:
    def __init__(self, bucket_name, endpoint):
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint
        self.s3_client = boto3.client("s3", endpoint_url=self.endpoint_url)
        self.sns = boto3.client("sns",endpoint_url=self.endpoint_url)

    def handle_request(self, event):
        try:
            if 'body' not in event or not event['body']:
                return {
                    "statusCode": 400,
                    "body": "No se proporcionó ningún archivo en la solicitud."
                }

            file_data = base64.b64decode(event['body']) if event.get("isBase64Encoded", False) else event['body']

            if isinstance(file_data, str):
                file_data = file_data.encode("utf-8")

            file_name = self.generate_filename(event)

            self.upload_to_s3(file_data, file_name)
            return {
                "statusCode": 200,
                "body": f"Archivo subido correctamente como {file_name}.",
                "file_name" : file_name
            }
        except Exception as e:
            print("[ERROR]", str(e))
            traceback.print_exc()
            return {
                "statusCode": 500,
                "body": f"Error al procesar la solicitud: {str(e)}"
            }

    def generate_filename(self, event):
        timestamp = int(time.time() * 1000)  
        return f"audio_{timestamp}.webm" 

    def upload_to_s3(self, file_data, file_name):
        try:
            print(f"[INFO] Subiendo {file_name} a {self.bucket_name}")
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_data,
                ContentType="audio/webm"
            )
        except Exception as e:
            raise RuntimeError(f"Error subiendo archivo a S3: {e}")

    def notify_glue(self, file_name, topic_arn):
        try:
            response = self.sns.publish(
                TopicArn=topic_arn,
                Message=f'{{"bucket_name": "{self.bucket_name}", "file_name": "{file_name}"}}',
            )
            
            print(f"Notificación enviada exitosamente: {response}")
        except Exception as e:
            print(f"[ERROR] Falló la publicación al tema SNS: {e}")

    def _response(self, status_code, message):
        return {
            "statusCode": status_code,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": message
        }


