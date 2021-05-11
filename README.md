# Run project

    1. Create Dynamodb table:  Use the table struture mentioned at https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
    2. Initalised the poetry : poetry init
    3. Start shell if not active any :  poetry shell
    4. python -m  uvicorn myapp.main:app --reload --port 8000

# Run pytest:

    python -m pytest . -v

# Resources:

    1. https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
    
    2. https://python-poetry.org/docs/basic-usage/
    
    3. https://pypi.org/project/mangum/
    
    5. How to deploy code to api and Lambda : https://www.youtube.com/watch?v=6fE31084Uks
    
    
    
    
# Sample output:

![image](https://user-images.githubusercontent.com/32964784/117859589-0ec14700-b244-11eb-8f9d-49e8977d2f39.png)
