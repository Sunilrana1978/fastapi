from typing import List

from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, HTTPException
from starlette import status

from ..repository import image, schemas

router = APIRouter()

import boto3
from botocore.exceptions import ClientError


@router.post("/",status_code=status.HTTP_201_CREATED,
    summary="Create a new Image",
    description="Create a new Image and Increment Version or create new image")
async def root(request:List[schemas.image]):
    """
    1. Check for the image (exists) => pk(image_name), sk.begins_with("v_")
    2. Increment Version or create new image
    """
    for item in request:
        image_resp = image.create_image(item.image_name , item.image_id,item.attributes,item.create_dt)
    return {"Record Saved"}

@router.get("/list_latest_images",status_code=status.HTTP_200_OK,
    summary="Get list  of latest images", 
    description="Get list  of latest images")
async def root():
    res_image = image.list_latest_images()
    if not res_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No images found')
    return res_image.get('Items')


@router.get("/get_latest_image_by_name",status_code=status.HTTP_200_OK)
async def root(image_name:str):
    res_image = image.get_latest_image_by_name(image_name)
    if not res_image.get('Item'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The image with name {image_name}  not found')
    if res_image:
        print("Get image succeeded:")
    return  res_image.get('Item')


@router.get("/get_specific_image_by_name_and_version",status_code=status.HTTP_200_OK)
async def root(image_name:str,version:int):
    res_image = image.get_specific_image_by_name_and_version(image_name,version)
    if not res_image.get('Item'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The image with name {image_name}  not found')
    if res_image:
        print("Get image succeeded:")
    return  res_image.get('Item')

