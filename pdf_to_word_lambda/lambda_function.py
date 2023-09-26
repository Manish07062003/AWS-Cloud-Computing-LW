import boto3
from pdf2docx import Converter
from io import BytesIO

def lambda_handler(event, context):
    # Set up the S3 client
    s3 = boto3.client('s3')

    # Define the source and destination bucket names
    source_bucket = 'myofficetopdfconversionbucket'
    destination_bucket = 'mypdfoutputbucket'

    # Retrieve the S3 object from the event
    s3_event_record = event['Records'][0]['s3']
    object_key = s3_event_record['object']['key']

    # Download the PDF file from S3
    response = s3.get_object(Bucket=source_bucket, Key=object_key)
    pdf_content = response['Body'].read()

    # Convert the PDF to Word document
    docx_content = convert_to_docx(pdf_content)

    # Upload the converted Word document to the destination bucket
    docx_key = object_key[:-4] + '.docx'
    s3.put_object(Bucket=destination_bucket, Key=docx_key, Body=docx_content, ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    return {
        'statusCode': 200,
        'body': 'PDF to Word conversion successful!',
    }

def convert_to_docx(pdf_content):
    # Use pdf2docx to convert the PDF content to a Word document
    docx_output = BytesIO()
    with Converter(BytesIO(pdf_content)) as converter:
        converter.convert(docx_output)
    docx_content = docx_output.getvalue()

    return docx_content

