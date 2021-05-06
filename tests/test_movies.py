# """
# Example of using moto to mock out DynamoDB table
# """
 
# import boto3
# from moto import mock_dynamodb2
# from fastapi.testclient import TestClient
# from myapp.main import app
# import store_data
 
# @mock_dynamodb2
# def test_write_into_table():
#     "Test the write_into_table with a valid input data"
#     dynamodb = boto3.resource('dynamodb')
#     table_name = 'Movies'
#     table = dynamodb.create_table(TableName='Movies',
#         KeySchema=[
#             {
#                 'AttributeName': 'year',
#                 'KeyType': 'HASH'  # Partition key
#             },
#             {
#                 'AttributeName': 'title',
#                 'KeyType': 'RANGE'  # Sort key
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'year',
#                 'AttributeType': 'N'
#             },
#             {
#                 'AttributeName': 'title',
#                 'AttributeType': 'S'
#             },

#         ])
    
#     data = {
#         "year": 2016,"title": "Rush",
#         "info": {
#             "plot": "A re-creation of the merciless 1970s rivalry between Formula One rivals James Hunt and Niki Lauda.",
#             "rating": 8.3
#             }
#         }
#     store_data.write_into_table(data,table_name)
#     response = table.get_item(Key={'date':data['date']})
#     actual_output = response['Item']
#     assert actual_output == data


