import boto3
import os
from io import BytesIO
from docx2pdf import convert  # Requires 'docx2pdf' package. You can install it with 'pip install docx2pdf'

def lambda_handler(event, context):
    # Set up the S3 client
    s3 = boto3.client('s3')

    # Define the source and destination bucket names
    source_bucket = 'your-source-bucket-name'
    destination_bucket = 'your-destination-bucket-name'

    # Retrieve the S3 object from the event
    s3_event_record = event['Records'][0]['s3']
    object_key = s3_event_record['object']['key']
    file_name, file_extension = os.path.splitext(os.path.basename(object_key))

    # Download the file from S3
    response = s3.get_object(Bucket=source_bucket, Key=object_key)
    file_content = response['Body'].read()

    # Convert the office document to PDF
    if file_extension in ['.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt']:
        pdf_content = convert(BytesIO(file_content))
    else:
        # If the file is not a supported office document, you can handle the error accordingly.
        raise ValueError(f"Unsupported file format: {file_extension}")

    # Upload the converted PDF to the destination bucket
    pdf_key = f"{file_name}.pdf"
    s3.put_object(Bucket=destination_bucket, Key=pdf_key, Body=pdf_content, ContentType='application/pdf')

    return {
        'statusCode': 200,
        'body': 'File conversion successful!',
    }

