from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class movie_info(BaseModel):
    plot: str = " "
    rating: int 

class movie(BaseModel):
    year: int
    title: str
    info: movie_info

class image(BaseModel):
    image_name: str
    image_id: str
    attributes:str
    create_dt:datetime