import pandas as pd

import Interoperability as io

# Sample source and target dataframes for illustration
source_data = {
    'UID': [1, 2, 3, 4],
    'Name': ['Alice', 'Bobi', 'Charlie', 'David'],
    'Address': ['Alice dale', 'Bob dale', 'Charlie dale', 'David dale'],
    'Age': [25, 30, 35, 40]
}

target_data = {
    'UID': [1, 2, 3, 5],
    'Name': ['Alice', 'Bobi', 'Charlie', 'Eva'],
    'Address': ['Alice dale', 'Bobi dale', 'Charlie dale', 'Eva dale'],
    'Age': [25, 30, 35, 28]
}

source_df = pd.DataFrame(source_data)
target_df = pd.DataFrame(target_data)

# Key columns for matching
key_columns = 'UID'

# Perform cell-by-cell comparison and tag mismatches
reconciliation_results = io.data_integration_reconciliation(source_df, target_df, key_columns)




result_csv_file_path = '/Users/rajithprabhakaran/Desktop/result.csv'
reconciliation_results.to_csv(result_csv_file_path, index=False)