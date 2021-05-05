from fastapi import APIRouter,HTTPException
from starlette import status
from boto3.dynamodb.conditions import Key
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# Let's use Amazon S3
s3 = boto3.resource('s3')

dbb_url="https://dynamodb.us-east-1.amazonaws.com"

def get_movie(year,title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.Table('Movies')

    try:
        response = table.get_item(Key={'year': year, 'title': title})   
        if 'Item' in response :
            result=response['Item']
        else:
            result = False

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return result

def put_movie(title, year, plot, rating, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.Table('Movies')
    response = table.put_item(
       Item={
            'year': year,
            'title': title,
            'info': {
                'plot': plot,
                'rating': rating
            }
        }
    )
    return response

def delete_underrated_movie(year:int,title:str, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
     
    table = dynamodb.Table('Movies')

    try:
        response = table.delete_item(
            Key={
                'year': year,
                'title': title
            }
        )
    except ClientError as e:
        return e.response['Error']['Message']
    else:
        return response


def query_movies(year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.Table('Movies')
    response = table.query(
        KeyConditionExpression=Key('year').eq(year)
    )
    return response['Items']


def update_movie(year,title, rating, plot, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.Table('Movies')

    response = table.update_item(
        Key={
            'year': year,
            'title': title
        },
        UpdateExpression="set info.rating=:r, info.plot=:p",
        ExpressionAttributeValues={
            ':r': Decimal(rating),
            ':p': plot
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def load_movies(movies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.Table('Movies')
    for movie in movies:
        year = movie["year"]
        title = movie["title"]
        rating = movie["info"]["rating"]
        table.put_item(Item={
            'year': year,
            'title': title,
            'info': {
                'plot':movie["info"]["plot"],
                'rating': rating
            }
        })