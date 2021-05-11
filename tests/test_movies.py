import json
import unittest
from pprint import pprint
from unittest import mock

import boto3
import pytest
import simplejson as json
from botocore.exceptions import ClientError
from moto import mock_dynamodb2


@mock_dynamodb2
@pytest.mark.usefixtures('put_Movies_str')
class TestDatabaseFunctions(unittest.TestCase):
    
    def setUp(self)->None:
        """Setup function to create the database and global variable """
        #Create the mock database and table
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')   
        #create the table    
        from myapp.api.repository.MoviesCreateTable import create_movie_table
        self.table = create_movie_table(self.dynamodb) 

        # Create variable to store the expected output for testcase validation
        self.expeted_response={
            'Items':[
                {
                "year": self.put_Movies_str.year,
                "info": {
                    "rating": self.put_Movies_str.rating,
                    "plot": self.put_Movies_str.plot
                },
                "title":self.put_Movies_str.title}
            ]
        }
        #create fastapi test clinet
        from fastapi.testclient import TestClient
        from myapp.main import app
        self.client = TestClient(app)  

   
    # start: Testing the dynamodb operation directly 

    def tearDown(self)->None:
        """Delete mock database and table after test is run"""
        self.table.delete()
        self.dynamodb=None

    def test_1_table_exists(self)->None:
        self.assertTrue(self.table) # check if we got a result
        self.assertIn('Movies', self.table.name) # check if the table name is 'Movies'
        pprint(self.table.name)

    def test_2_put_movie(self)->None:
        """Test the put function"""
        from myapp.api.repository.movies import put_movie 

        result =  put_movie(self.put_Movies_str.title,self.put_Movies_str.year,self.put_Movies_str.plot,self.put_Movies_str.rating)
        
        self.assertEqual(200, result['ResponseMetadata']['HTTPStatusCode'])
        pprint(result)

    def test_3_get_movie(self)->None:
       """Test the get function"""
       from myapp.api.repository.movies import get_movie, put_movie

       put_movie(self.put_Movies_str.title,self.put_Movies_str.year,self.put_Movies_str.plot,self.put_Movies_str.rating)

       result = get_movie(self.put_Movies_str.year,self.put_Movies_str.title)

       self.assertEqual(self.put_Movies_str.year, result['year'])
       self.assertEqual(self.put_Movies_str.title, result['title'])

 
    # End: Testing the dynamodb operation directly 
    

    
    # start: Testing the Api end points 
   
    def test_4_get_movie_with_year(self)->None:
        """Test the get api with path parameter function"""
        from myapp.api.repository.movies import get_movie, put_movie
        put_movie(self.put_Movies_str.title,self.put_Movies_str.year,self.put_Movies_str.plot,self.put_Movies_str.rating)
         
        response = self.client.get(f"/v1/movies/{self.put_Movies_str.year}")
        assert response.status_code == 200
        assert response.json() == self.expeted_response['Items']

    def test_4_get_movie_with_year_not_exists(self)->None:
        """Test the get api with path parameter function"""
        from myapp.api.repository.movies import get_movie, put_movie
        put_movie(self.put_Movies_str.title,self.put_Movies_str.year,self.put_Movies_str.plot,self.put_Movies_str.rating)
   
        response = self.client.get(f"/v1/movies/{2016}")
        assert response.status_code == 404
    
    def test_5_get_movie_with_year_title(self)->None:
        """Test the get api with path parameter function"""
        from myapp.api.repository.movies import get_movie, put_movie
        put_movie(self.put_Movies_str.title,self.put_Movies_str.year,self.put_Movies_str.plot,self.put_Movies_str.rating)

        response = self.client.get(f"/v1/movies/?year={self.put_Movies_str.year}&title={self.put_Movies_str.title}")
        assert response.status_code == 200
        assert response.json() == self.expeted_response['Items'][0]

    def test_5_get_movie_with_year_title_not_exists(self)->None:
        """Test the get api with path parameter function"""
        from myapp.api.repository.movies import get_movie, put_movie
        put_movie(self.put_Movies_str.title,self.put_Movies_str.year,self.put_Movies_str.plot,self.put_Movies_str.rating)
 
        response = self.client.get(f"/v1/movies/?year={2016}&title={self.put_Movies_str.title}")
        assert response.status_code == 404
    
    def test_6_delete_movie_with_year_title(self)->None:
        """Test the delete api with query parameter function"""
        from myapp.api.repository.movies import (delete_underrated_movie,
                                                 get_movie, put_movie)

        put_movie(self.put_Movies_str.title,self.put_Movies_str.year,self.put_Movies_str.plot,self.put_Movies_str.rating)
        
        Delete_response = self.client.delete(f"/v1/movies/?year={self.put_Movies_str.year}&title={self.put_Movies_str.title}")

        assert Delete_response.status_code == 200

        response = self.client.get(f"/v1/movies/?year={2016}&title={self.put_Movies_str.title}")
        assert response.status_code == 404

    def test_7_post_movie(self)->None:
        """Test the delete api with query parameter function"""
        from myapp.api.repository.movies import (delete_underrated_movie,
                                                 get_movie, put_movie)

        payload =[ {"year": self.put_Movies_str.year,
                    "title": self.put_Movies_str.title,
                    "info": {
                        "plot": self.put_Movies_str.plot,
                        "rating": self.put_Movies_str.rating}
                    }
                ]

        payload=json.dumps(payload)

        post_response = self.client.post("/v1/movies/",data=payload)
        
        assert post_response.status_code == 201

        response = self.client.get(f"/v1/movies/?year={self.put_Movies_str.year}&title={self.put_Movies_str.title}")
        assert response.status_code == 200
    
    #End: Testing the Api end points 
    
