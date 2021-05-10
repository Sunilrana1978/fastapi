import pytest 
from fastapi import  Request
class Movie:

    def __init__(self, title, year, plot, rating):
        self.title = title
        self.year = year
        self.plot = plot
        self.rating = rating


@pytest.fixture(scope="class")
def put_Movies_str(request: Request):
    request.cls.put_Movies_str = Movie("The Big New Movie",2015,
                           "Nothing happens at all.", 0)
    

