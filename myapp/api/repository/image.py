from boto3.dynamodb.conditions import Key
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

dbb_url="https://dynamodb.us-east-1.amazonaws.com"
dynamodb = boto3.resource('dynamodb', endpoint_url=dbb_url)
table = dynamodb.Table("single-table")

def create_image(image_name, image_id,attributes,create_dt, dynamodb=dbb_url):
    """
    1. Check for the image (exists) => pk(image_name), sk.begins_with("v_")
    2. Increment Version or create new image
    """
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    existing_images = table.query(KeyConditionExpression = Key("pk").eq(image_name) & Key("sk").begins_with("v_"))
    if 'Items' in existing_images and existing_images.get('Items'):
        num_versions = len(existing_images.get('Items'))
        table.put_item(Item={"pk": image_name, "sk": "v_{}".format(num_versions + 1), "image_id": image_id,"attributes": attributes,"create_dt":str(create_dt)})
        table.put_item(Item={"pk": "image", "sk": "v0#{}".format(image_name), "image_id": image_id,"attributes": attributes,"create_dt":str(create_dt)})
    else:
        table.put_item(Item={"pk": image_name, "sk": "v_1", "image_id": image_id,"attributes": attributes,"create_dt":str(create_dt)})
        table.put_item(Item={"pk": "image", "sk": "v0#{}".format(image_name), "image_id": image_id,"attributes": attributes,"create_dt":str(create_dt)})

def list_latest_images(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    list_images = table.query(KeyConditionExpression=Key("pk").eq("image") & Key("sk").begins_with("v0#"))
    print(list_images.get('Items'))
    return list_images

def get_latest_image_by_name(image_name,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    specific = table.get_item(Key = {"pk": "image", "sk": f"v0#{image_name}"})
    print(specific.get('Item'))
    return specific

def get_specific_image_by_name_and_version(image_name, version,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    older_version = table.get_item(Key = {"pk": image_name, "sk": f"v_{version}"})
    print(older_version.get('Item'))
    return older_version

