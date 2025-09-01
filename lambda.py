import uuid
import boto3
import json


def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('eventDB')

        # Extract data directly from event
        event_id = str(uuid.uuid4())
        name = event.get('name')
        age = event.get('age')
        email = event.get('email')
        event_name = event.get('event')

        # Debug logging
        print(f"Event data: {event}")
        print(f"Name: {name}, Age: {age}, Email: {email}, EventName: {event_name}")

        # Validate required fields
        if not all([name, age, email, event_name]):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required fields',
                    'received': {
                        'Name': name,
                        'Age': age,
                        'Email': email,
                        'EventName': event_name
                    }
                })
            }

        # Insert into DynamoDB
        table.put_item(Item={
            'eventID': event_id,
            'Name': name,
            'Age': int(age) if age else None,
            'Email': email,
            'EventName': event_name
        })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Registration successful',
                'eventID': event_id
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }