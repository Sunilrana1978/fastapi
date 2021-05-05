# from fastapi.testclient import TestClient

# from unittest.mock import MagicMock, call
# import boto3

# import pytest

# from myapp.main import app

# client = TestClient(app)

# def test_read_main():
#     response = client.get("/v1/users")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}



# def test_query_movies(make_stubber):
#     dyn = boto3.resource('dynamodb')
#     dyn_stubber = make_stubber(dyn.meta.client)
#     year = 1969
#     stub_movies = [{
#         'title': f'Test {index}',
#         'year': year,
#         'info': f'An extra {index} units of informational data.'
#     } for index in range(1, 10)]

#     dyn_stubber.stub_query('Movies', stub_movies, key_condition=Key('year').eq(year))

#     movies = MoviesQuery01.query_movies(year, dynamodb=dyn)
#     assert movies == stub_movies