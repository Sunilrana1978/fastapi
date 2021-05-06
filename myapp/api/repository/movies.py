from fastapi import APIRouter,HTTPException
from starlette import status
from boto3.dynamodb.conditions import Key
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from .dynamodb import ddb

db=ddb("https://dynamodb.us-east-1.amazonaws.com","Movies")
table=db.create_connection()

def put_movie(title, year, plot, rating):
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

def get_movie(year,title):
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


def delete_underrated_movie(year:int,title:str):
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


def query_movies(year):
    response = table.query(
        KeyConditionExpression=Key('year').eq(year)
    )
    return response['Items']


def update_movie(year,title, rating, plot):
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

def load_movies(movies):
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