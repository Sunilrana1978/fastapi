
import pytest 
from fastapi import  Request
from typing import Type
from pydantic import BaseModel, Field
from decimal import Decimal

# Class to mimic movies object/record.
# class Movie():
#     """Class to mimic movies object/record."""
#     def __init__(self, title:str, year:int, plot:str, rating):
#         self.title = title
#         self.year = year
#         self.plot = plot
#         self.rating = rating

# @pytest.fixture(scope="class")
# def put_Movies_str(request: Request) -> Movie:
#     """Fixture to create globle put record object."""
#     request.cls.put_Movies_str = Movie(title="The Big New Movie"
#                                 ,year=2015
#                                 ,plot="Nothing happens at all."
#                                 ,rating=0)
class Movie1(BaseModel):
        title: str
        year:int
        plot:str
        rating:Decimal 

# Fixture to create globle put record object.
@pytest.fixture(scope="class")
def put_Movies_str(request: Request) -> Movie1:
    """Fixture to create globle put record object."""
    request.cls.put_Movies_str = Movie1(title="The Big New Movie"
                                ,year=2015
                                ,plot="Nothing happens at all."
                                ,rating=0.0)
    

