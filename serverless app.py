import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the uploaded image from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download the image
    image_object = s3.get_object(Bucket=bucket, Key=key)
    image_content = image_object['Body'].read()

    # Resize the image using PIL
    image = Image.open(io.BytesIO(image_content))
    image = image.resize((200, 200))  # Resize to 200x200

    # Save the image to a new location
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)

    s3.put_object(Bucket=bucket, Key=f"resized-{key}", Body=buffer, ContentType='image/jpeg')
    
    return {
        'statusCode': 200,
        'body': 'Image resized and saved!'
    }
