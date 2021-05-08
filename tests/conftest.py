import pytest

class Movie:

    def __init__(self, title, year, plot, rating):
        self.title = title
        self.year = year
        self.plot = plot
        self.rating = rating


# @pytest.fixture(scope='session', autouse=True)
def put_Movies_str():
    return Movie("The Big New Movie",2015,
                           "Nothing happens at all.", 0)