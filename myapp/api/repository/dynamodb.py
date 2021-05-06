

import boto3

class ddb:
    def __init__(self,dbb_url,table_name):
        self.dbb_url=dbb_url
        self.table_name=table_name
     
    def create_connection(self):
        dbb_url=self.dbb_url
        dynamodb = boto3.resource('dynamodb', endpoint_url=dbb_url)
        table = dynamodb.Table(self.table_name)
        return table
