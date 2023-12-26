import Validity as vl
import pandas as pd
from datetime import datetime

def processor():
    df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
    print(vl.is_date_in_dataset(df,'%Y-%m-%d %H:%M:%S'))

def test():
    import pandas as pd

    # Read the CSV file
    df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
    column_name = 'product_description'

    def contains_only_text(value):
        return all(char.isalpha() or not char.isnumeric() for char in str(value))

    df[f'{column_name}_contains_only_text'] = df[column_name].apply(lambda x: contains_only_text(x))
    print(df)

def lambda_example():
    # Regular function to add two numbers
    def add1(x, y):
        return x + y

    # Equivalent lambda function
    lambda_add = lambda x, y: x + y

    # Using the functions
    result_regular = add1(3, 5)
    result_lambda = lambda_add(3, 5)

    print("Regular function result:", result_regular)
    print("Lambda function result:", result_lambda)

if __name__ == "__main__":
    processor()
    #test()
    #lambda_example