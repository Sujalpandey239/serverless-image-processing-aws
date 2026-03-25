import boto3
import os
import urllib.parse
from PIL import Image, ImageDraw
import io
import json

# Initialize AWS Clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# --- CONFIGURATION (Professional Method: Environment Variables) ---
# These are fetched from the 'Configuration' tab in your Lambda console
INPUT_BUCKET  = os.environ.get('INPUT_BUCKET', 'sujal-input-images')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'sujal-output-images')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:669493203560:image-processing-updates')

SIZES = {'thumbnail': (150, 150), 'medium': (500, 500), 'large': (1024, 1024)}
WATERMARK_TEXT = "Sujal | AWS Project"

def add_watermark(image):
    """Adds a Sujal-branded watermark to the bottom-right of the image."""
    draw = ImageDraw.Draw(image)
    img_width, img_height = image.size
    
    # Calculate position
    text_width = len(WATERMARK_TEXT) * 7
    text_x, text_y = img_width - text_width - 10, img_height - 25
    
    # Draw dark background for text visibility
    draw.rectangle([text_x - 5, text_y - 5, text_x + text_width + 5, text_y + 20], fill=(0, 0, 0, 160))
    draw.text((text_x, text_y), WATERMARK_TEXT, fill=(255, 255, 255, 255))
    return image

def lambda_handler(event, context):
    file_key = "Unknown"
    source = "Unknown"
    
    try:
        # 1. Identify Trigger Source (S3 vs API Gateway)
        if 'Records' in event:
            # S3 Automatic Trigger
            record = event['Records'][0]
            file_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
            source = "S3 Automatic Upload"
        elif 'body' in event:
            # API Gateway / Postman Trigger
            body = json.loads(event['body'])
            file_key = body.get('image_name')
            source = "API Gateway (Postman)"
        else:
            return {"statusCode": 400, "body": json.dumps("Unsupported trigger source")}

        if not file_key:
            return {"statusCode": 400, "body": json.dumps("No file key provided")}

        # 2. Process Image from S3
        print(f"Downloading {file_key} from {INPUT_BUCKET}...")
        response = s3.get_object(Bucket=INPUT_BUCKET, Key=file_key)
        original = Image.open(io.BytesIO(response['Body'].read()))
        
        # Convert to RGB if necessary (handles PNG/RGBA)
        if original.mode in ('RGBA', 'P', 'LA'):
            original = original.convert('RGB')

        base_name = os.path.splitext(os.path.basename(file_key))[0]

        # Process variants
        for folder, (max_w, max_h) in SIZES.items():
            img = original.copy()
            img.thumbnail((max_w, max_h), Image.LANCZOS)
            img = add_watermark(img)
            
            # Save to memory buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            
            # Upload to Output Bucket
            output_path = f"{folder}/{base_name}.jpg"
            s3.put_object(
                Bucket=OUTPUT_BUCKET, 
                Key=output_path, 
                Body=buffer, 
                ContentType='image/jpeg'
            )
            print(f"Successfully saved {output_path}")

        # 3. Send SNS Notification
        success_message = (
            f"Hello Sujal,\n\n"
            f"Image Processing Successful!\n"
            f"File: {file_key}\n"
            f"Trigger: {source}\n"
            f"Variants created: {list(SIZES.keys())}\n"
            f"Bucket: {OUTPUT_BUCKET}"
        )
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=success_message,
            Subject="🚀 AWS Project: Processing Complete"
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Success", 
                "file": file_key, 
                "notification": "Email sent"
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
