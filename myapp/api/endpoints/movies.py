import simplejson as json
import os
from decimal import Decimal
from typing import List

from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from starlette import status

from ..repository import movies, schemas

router = APIRouter()

import boto3
from botocore.exceptions import ClientError


@router.get("/",status_code=status.HTTP_200_OK)
async def root(year:int,title:str) -> dict:
    movie = movies.get_movie(year,title)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Movies with year {year} and title {title} not found')
    if movie:
        print("Get movie succeeded:")
    return movie

@router.post("/",status_code=status.HTTP_201_CREATED)
async def root(request:List[schemas.movie])->str:
    for item in request:
        movie_resp = movies.put_movie(item.title , item.year,item.info.plot,item.info.rating)
    return {"Record Saved"}

@router.delete("/")
async def root(year:int,title:str) -> dict:
    delete_response = movies.delete_underrated_movie(year,title)
    if not delete_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Movies with year {year} and title {title} not found')
    return  {"Record deleted":delete_response}

@router.get("/{year}",status_code=status.HTTP_200_OK)
async def root(year:int) -> dict:
    movie = movies.query_movies(year)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Movies with year {year}  not found')
    return movie

@router.put("/", status_code=status.HTTP_202_ACCEPTED)
async def root(request:schemas.movie)->str:
    update_response = movies.update_movie(request.year,request.title, request.info.rating, request.info.plot)
    if update_response:
        print("Delete movie succeeded:")
    if not update_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The Movies with year {year} and title {title} not found')
    return  {"Record Updated"}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(file.filename) as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    
    movies.load_movies(movie_list)

    return movie_list


@router.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }



    
   