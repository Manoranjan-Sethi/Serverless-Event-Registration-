import uuid
import boto3
import json

def lambda_handler(event, context):
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
    
    # Handle OPTIONS (preflight) request
    method = event.get('httpMethod', None)
    if method == 'OPTIONS':
        return {        
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Handle POST request
    if method == 'POST':
        try:
            dynamodb = boto3.resource('dynamodb') 
            table = dynamodb.Table('eventDB')
            sns = boto3.client('sns')
            
            # Parse body
            body = json.loads(event['body'])
            
            # Extract data
            event_id = str(uuid.uuid4())
            name = body.get('Name')
            age = body.get('Age')
            email = body.get('Email')
            event_name = body.get('EventName')
            
            # Debug logging
            print(f"Received data: Name={name}, Age={age}, Email={email}, EventName={event_name}")
            
            # Insert into DynamoDB
            table.put_item(Item={
                'eventID': event_id,
                'Name': name,
                'Age': int(age) if age and age.isdigit() else None,
                'Email': email,
                'EventName': event_name
            })

            # 🔔 Publish SNS notification
            sns.publish(
                TopicArn='arn:aws:sns:ap-south-1:442426869902:Form-Notify-Mailer',
                Subject='Event Registration Confirmation',
                Message=f"Hi {name}, your registration for '{event_name}' has been received successfully!"
            )

            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'message': 'Registration successful',
                    'eventID': event_id
                })
            }
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': f'Internal server error: {str(e)}'
                })
            }
    
    # Method not allowed
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed'})
    }