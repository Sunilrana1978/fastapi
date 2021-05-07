import simplejson as json
from pprint import pprint
import unittest
from unittest import mock
import boto3
from botocore.exceptions import ClientError
from moto import mock_dynamodb2

@mock_dynamodb2
class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        """Create the mock database and table"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        from myapp.api.repository.MoviesCreateTable import create_movie_table
        self.table = create_movie_table(self.dynamodb) 
    
    def tearDown(self):
        """Delete mock database and table after test is run"""
        self.table.delete()
        self.dynamodb=None

    def test_table_exists(self):
        self.assertTrue(self.table) # check if we got a result
        self.assertIn('Movies', self.table.name) # check if the table name is 'Movies'
        pprint(self.table.name)

    def test_put_movie(self):
        """Test the put function"""
        from myapp.api.repository.movies import put_movie 

        result = put_movie("The Big New Movie",2015,
                           "Nothing happens at all.", 0)
        
        self.assertEqual(200, result['ResponseMetadata']['HTTPStatusCode'])
        pprint(result)

    def test_get_movie(self):
       """Test the get function"""
       from myapp.api.repository.movies import put_movie ,get_movie
       result1 = put_movie("The Big New Movie",2015,
                           "Nothing happens at all.", 0)
       result = get_movie(2015,"The Big New Movie")

       self.assertEqual(2015, result['year'])
       self.assertEqual("The Big New Movie", result['title'])
       self.assertEqual("Nothing happens at all.", result['info']['plot'])
       self.assertEqual(0, result['info']['rating'])


@mock.patch("myapp.api.repository.movies.table.query") 
def test_get_movie_api(mock_requests_get):
    expeted_response={
        'Items':[
            {
            "year": 2015,
            "info": {
                "rating": 0,
                "plot": "Nothing happens at all."
            },
            "title": "The Big New Movie"}
        ]
    }
    mock_requests_get.return_value = mock.Mock(name="mock response",
                                               **{"status_code": 200, "json.return_value": expeted_response})
    from fastapi.testclient import TestClient
    from myapp.main import app
    client = TestClient(app)   
    response = client.get("/v1/movies/2015")
    
    assert response.status_code == 200
    assert response.json() == expeted_response['Items']