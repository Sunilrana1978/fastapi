import pytest 
from fastapi import  Request

# Class to mimic movies object/record.
class Movie:
    """Class to mimic movies object/record."""
    def __init__(self, title, year, plot, rating):
        self.title = title
        self.year = year
        self.plot = plot
        self.rating = rating


# Fixture to create globle put record object.
@pytest.fixture(scope="class")
def put_Movies_str(request: Request):
    """Fixture to create globle put record object."""
    request.cls.put_Movies_str = Movie("The Big New Movie",2015,
                           "Nothing happens at all.", 0)
    

